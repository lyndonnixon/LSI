# -*- coding: UTF-8 -*-
"""Encapsulation of the invokers of Web APIs, and the functionality of contextual query.

.. moduleauthor:: Dong Liu <liu.dong66@gmail.com>
"""
import socket
import threading
from datetime import datetime
from datetime import timedelta
from time import sleep
import urllib
import httplib2
from lxml import etree
from dateutil import parser as dateparser
from instagram.client import InstagramAPI
from foursquare import Foursquare
import model
import json
from linkeddata import LinkedData
import ner as ner_service
import math
import esclient
import config
import logging
from utils import timeout


class OokabooAPI(object):
    """Wrapper of Ookaboo API."""
    def __init__(self):
        self.api_name = 'Ookaboo API'

    def invoke(self, lod, context=None):
        """Invoke Ookaboo API with a LOD resource and a context.

        Args:
            lod (object): instance of linkeddata.LinkedData

            context (object): instance of linkeddata.LinkedData

        Returns:
            (list): a list of images
        """
        # prepare request
        body = {'query_uri': lod.uri, 'api_key': 'MjE0YzU5NmJi'}
        request = 'http://api.ookaboo.com/api1/lookup_picture?' + urllib.urlencode(body)
        response, content = httplib2.Http().request(request, 'GET')
        if response.status == 200:
            return self._parse_results(content, lod, context)
        else:
            raise IOError('Fail to invoke Ookaboo API: ' + request)

    def _parse_results(self, ookaboo_json, lod, context):
        # parse response
        image_list = []
        json_obj = json.loads(ookaboo_json)
        if json_obj['success']:
            try:
                title = json_obj['result']['topic']['title']
            except:
                title = None
            for pic in json_obj['result']['pictures']:
                try:
                    author_name = pic['sources'][0]['title']
                    author_uri = pic['sources'][0]['source_uri']
                except:
                    author_name = None
                    author_uri = None
                for img in pic['images']:
                    if img['size_code'] == 'm':
                        image = model.Image()
                        image.source = "Ookaboo"
                        image.title = title
                        image.locator = img['img_uri']
                        image.height = img['height']
                        image.width = img['width']
                        image.auothor_name = author_name
                        image.author_uri = author_uri
                        image.query_lod = lod.uri
                        if context:
                            image.query_context = context.uri
                        image_list.append(image)
                        break
        return image_list

    def loop_invoke(self, lod, context):
        """Iteratively invoke Ookaboo API with a LOD resource and a context, and save the results into ElasticSearch.

        Args:
            lod (object): instance of linkeddata.LinkedData

            context (object): instance of linkeddata.LinkedData
        """
        try:
            media_resources = self.invoke(lod, context)
            # add to elasticsearch
            elastic_search_client = esclient.ElasticSearchClient(config.elastic_search_endpoint)
            for m in media_resources:
                if not elastic_search_client.find_media_by_locator(m.locator):
                    if isinstance(m, model.VideoTrack):
                        elastic_search_client.index_video(json.dumps(m, cls=model.VideoEncoder))
                    elif isinstance(m, model.Image):
                        elastic_search_client.index_image(json.dumps(m, cls=model.ImageEncoder))
        except Exception as e:
            logger = logging.getLogger('error')
            logger.error('Error in invoking Ookaboo API: ' + str(e))


class YouTubeAPI(object):
    """Wrapper of YouTube API."""
    def __init__(self):
        self.api_name = 'YouTube API'
        self.total_results = 0L

    def _prepare_request(self, lod, context=None, start_index=1, max_results=20):
        # prepare request
        q = lod.label
        if context:
            q += " " + context.label
        body = {'q': q, 'start-index': start_index, 'max-results': max_results, 'v': 2}
        request = 'https://gdata.youtube.com/feeds/api/videos?' + urllib.urlencode(body)
        return request

    def invoke(self, lod, context=None, start_index=1, max_results=20):
        """Invoke YouTube API with a LOD resource and a context.

        Args:
            lod (object): instance of linkeddata.LinkedData

            context (object): instance of linkeddata.LinkedData

            start_index (integer): the starting index of results

            max_results (integer): the total number of results

        Returns:
            (list): a list of videos
        """
        # send request
        request = self._prepare_request(lod, context, start_index, max_results)
        response, content = httplib2.Http().request(request, 'GET')
        if response.status == 200:
            return self._parse_results(content, lod, context)
        else:
            raise IOError('Fail to invoke YouTube API: ' + request)

    def loop_invoke(self, lod, context):
        """Iteratively invoke YouTube API with a LOD resource and a context, and save the results into ElasticSearch.

        Args:
            lod (object): instance of linkeddata.LinkedData

            context (object): instance of linkeddata.LinkedData
        """
        self.total_results = 0L
        start_index = 1
        max_results = 50
        media_resources = self.invoke(lod, context, start_index=start_index, max_results=max_results)
#         print 'got total results:' + str(self.total_results)
        while (start_index + max_results) < self.total_results:
#             print 'start_index:' + str(start_index)
            start_index += max_results
            try:
                # add to elasticsearch
                elastic_search_client = esclient.ElasticSearchClient(config.elastic_search_endpoint)
                for m in media_resources:
                    if not elastic_search_client.find_media_by_locator(m.locator):
                        if isinstance(m, model.VideoTrack):
                            elastic_search_client.index_video(json.dumps(m, cls=model.VideoEncoder))
                        elif isinstance(m, model.Image):
                            elastic_search_client.index_image(json.dumps(m, cls=model.ImageEncoder))
                media_resources = self.invoke(lod, context, start_index=start_index, max_results=max_results)
            except Exception as e:
                logger = logging.getLogger('error')
                logger.error('Error in invoking YouTube API: ' + str(e))

    def _parse_results(self, youtube_xml, lod, context):
        # parse response
        video_list = []
        utf8_parser = etree.XMLParser(encoding='utf-8')
        feed = etree.fromstring(youtube_xml, parser=utf8_parser)
        # set total result for loop invoking
        if not self.total_results:
            self.total_results = long(feed.xpath('openSearch:totalResults/text()',
                                                 namespaces={'openSearch': 'http://a9.com/-/spec/opensearch/1.1/'})[0])
            if self.total_results > 1000:
                self.total_results = 1000
        # iteration
        for entry in feed.xpath('atom:entry', namespaces={'atom': 'http://www.w3.org/2005/Atom'}):
            video = model.VideoTrack()
            video.title = (entry.xpath('atom:title/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})[0]).encode('utf-8')
            video.published = datetime.strptime(entry.xpath('atom:published/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})[0], '%Y-%m-%dT%H:%M:%S.000Z')
            try:
                video.created = datetime.strptime(entry.xpath('yt:recorded/text()', namespaces={'yt': 'http://gdata.youtube.com/schemas/2007'})[0], '%Y-%m-%d')
            except:
                video.created = None
            try:
                video.description = (entry.xpath('.//media:description/text()', namespaces={'media': 'http://search.yahoo.com/mrss/'})[0]).encode('utf-8')
            except:
                video.description = None
            video.locator = str(entry.xpath('media:group/media:player/@url', namespaces={'media': 'http://search.yahoo.com/mrss/'})[0])
            video.duration = str(entry.xpath('media:group/yt:duration/@seconds', namespaces={'media': 'http://search.yahoo.com/mrss/', 'yt': 'http://gdata.youtube.com/schemas/2007'})[0])
            video.thumbnail = str(entry.xpath('media:group/media:thumbnail/@url', namespaces={'media': 'http://search.yahoo.com/mrss/'})[0])
            video.author_uri = entry.xpath('atom:author/atom:uri/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})[0]
            video.author_name = (entry.xpath('atom:author/atom:name/text()', namespaces={'atom': 'http://www.w3.org/2005/Atom'})[0]).encode('utf-8')
            try:
                lat_lng_string = entry.xpath('georss:where/gml:Point/gml:pos/text()', namespaces={'georss': 'http://www.georss.org/georss', 'gml': 'http://www.opengis.net/gml'})[0]
                video.latitude = lat_lng_string.split(' ')[0]
                video.longitude = lat_lng_string.split(' ')[1]
            except:
                video.latitude = None
                video.longitude = None
            try:
                video.location_name = entry.xpath('yt:location/text()', namespaces={'yt': 'http://gdata.youtube.com/schemas/2007'})[0]
            except:
                video.location_name = None
            video.width = None
            video.height = None
            video.source = "YouTube"
            video.query_lod = lod.uri
            if context:
                video.query_context = context.uri
            video_list.append(video)
        return video_list


class FlickrAPI(object):
    """Wrapper of Flickr API."""
    def __init__(self):
        self.api_name = 'Flickr API'
        self.total_page = 0

    def _prepare_request(self, lod, context=None, page=1):
        # prepare request
        q = lod.label
        if context:
            q += " " + context.label
        body = {'text': q}
        request = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&extras=description,date_upload&api_key=ca46db6f999837f739c431ca0bd2fb33&format=json&nojsoncallback=1&' \
                  + urllib.urlencode(body) + '&page=' + str(page)
        return request

    def invoke(self, lod, context=None, page=1):
        """Invoke Flickr API with a LOD resource and a context.

        Args:
            lod (object): instance of linkeddata.LinkedData

            context (object): instance of linkeddata.LinkedData

            page (integer): page number of the results
        Returns:
            (list): a list of images
        """
        # send request
        request = self._prepare_request(lod, context, page)
        response, content = httplib2.Http().request(request, 'GET')
        if response.status == 200:
            return self._parse_results(content, lod, context)
        else:
            raise IOError('Fail to invoke Flickr API: ' + request)

    def _parse_results(self, flickr_json, lod, context):
        image_list = []
        json_obj = json.loads(flickr_json)
        if json_obj['stat'] == 'ok':
            # save page num
            if not self.total_page:
                cl = logging.getLogger("crawler")
                cl.debug(json_obj['photos']['total'])
                self.total_page = int(math.ceil(int(json_obj['photos']['total']) / 100.0))
                if self.total_page > 2000:
                    self.total_page = 2000
            for photo in json_obj['photos']['photo']:
                image = model.Image()
                image.source = "Flickr"
                image.title = photo['title'].encode('utf-8')
                image.description = photo['description']['_content'].encode('utf-8').strip()
                image.published = datetime.fromtimestamp(int(photo['dateupload']))
                image.author_uri = 'http://www.flickr.com/photos/' + photo['owner']
                image.locator = "http://farm%s.staticflickr.com/%s/%s_%s.jpg" % (photo['farm'], photo['server'], photo['id'], photo['secret'])
                image.query_lod = lod.uri
                if context:
                    image.query_context = context.uri
                image_list.append(image)
        return image_list

    def loop_invoke(self, lod, context):
        """Iteratively invoke Flickr API with a LOD resource and a context, and save the results into ElasticSearch.

        Args:
            lod (object): instance of linkeddata.LinkedData

            context (object): instance of linkeddata.LinkedData
        """
        self.total_page = 0L
        media_resources = self.invoke(lod, context)
        for p in range(2, self.total_page + 1):
            cl = logging.getLogger('crawler')
            cl.debug("Flickr page: " + str(p) + '/' + str(self.total_page))
            try:
                elastic_search_client = esclient.ElasticSearchClient(config.elastic_search_endpoint)
                for m in media_resources:
                    if not elastic_search_client.find_media_by_locator(m.locator):
                        if isinstance(m, model.VideoTrack):
                            elastic_search_client.index_video(json.dumps(m, cls=model.VideoEncoder))
                        elif isinstance(m, model.Image):
                            elastic_search_client.index_image(json.dumps(m, cls=model.ImageEncoder))
                media_resources = self.invoke(lod, context, page=p)
            except Exception as e:
                logger = logging.getLogger('error')
                logger.error('Error in invoking Flickr API: ' + str(e))


class InstagramAPIWrapper(object):
    """Wrapper of Instagram API."""
    def __init__(self):
        self.api_name = 'Instagram API'
        self.api = InstagramAPI(client_id='4acda460e0c542c082b0b05c287f4630', client_secret='5362ffdba79842449190511df7124047')

    def _prepare_request(self, lod, context=None):
        if lod.lat:
            lat = lod.lat
        elif context and context.lat:
            lat = context.lat
        else:
            lat = None
        if lod.lng:
            lng = lod.lng
        elif context and context.lng:
            lng = context.lng
        else:
            lng = None
        # prepare request
        q = lod.label
        if context:
            q += " " + context.label
        return q, lat, lng

    def invoke(self, lod, context=None, min_timestamp=None, max_timestamp=None):
        """Invoke Instagram API with a LOD resource and a context.

        Args:
            lod (object): instance of linkeddata.LinkedData

            context (object): instance of linkeddata.LinkedData

            min_timestamp (integer): minimum value of the time stamp of the images

            max_timestamp (integer): maximum value of the time stamp of the images
        Returns:
            (list): a list of images
        """
        q, lat, lng = self._prepare_request(lod, context)
        if not lat:
            return []
        if not lng:
            return []
        # send request
        if min_timestamp and max_timestamp:
            media_resources = self.api.media_search(q=q, lat=float(lat), lng=float(lng), min_timestamp=min_timestamp, max_timestamp=max_timestamp)
        else:
            media_resources = self.api.media_search(q=q, lat=float(lat), lng=float(lng))
        image_list = []
        for media in media_resources:
            if media.caption:
                image = model.Image()
                image.source = "Instagram"
                image.title = media.caption.text
                image.published = dateparser.parse(str(media.created_time))
                image.locator = media.images['standard_resolution'].url
                image.width = media.images['standard_resolution'].width
                image.height = media.images['standard_resolution'].height
                try:
                    image.location_name = media.location.name
                    image.latitude = media.location.point.latitude
                    image.longitude = media.location.point.longitude
                except:
                    image.location_name = None
                    image.latitude = None
                    image.longitude = None
                try:
                    image.author_name = media.user.full_name
                    image.author_uri = 'http://instagram.com/' + media.user.username
                except:
                    image.author_name = None
                    image.author_uri = None
                image.query_lod = lod.uri
                if context:
                    image.query_context = context.uri
                image_list.append(image)
        return image_list

    def loop_invoke(self, lod, context):
        """Iteratively invoke Instagram API with a LOD resource and a context, and save the results into ElasticSearch.

        Args:
            lod (object): instance of linkeddata.LinkedData

            context (object): instance of linkeddata.LinkedData
        """
        media_resources = []
        max_time = datetime.utcnow()
        min_time = max_time - timedelta(5)
        early_time = max_time - timedelta(100)
        while max_time > early_time:
            max_time = min_time
            min_time = min_time - timedelta(5)
            try:
                media_resources = self.invoke(lod, context, min_time.strftime("%s"), max_time.strftime("%s"))
                # add to elasticsearch
                elastic_search_client = esclient.ElasticSearchClient(config.elastic_search_endpoint)
                for m in media_resources:
                    if not elastic_search_client.find_media_by_locator(m.locator):
                        if isinstance(m, model.VideoTrack):
                            elastic_search_client.index_video(json.dumps(m, cls=model.VideoEncoder))
                        elif isinstance(m, model.Image):
                            elastic_search_client.index_image(json.dumps(m, cls=model.ImageEncoder))
            except Exception as e:
                logger = logging.getLogger('error')
                logger.error('Error in invoking Instagram API: ' + str(e))
            sleep(3)


class FoursquareAPI(object):
    """Wrapper of Foursquare API."""
    def __init__(self):
        self.api = Foursquare(client_id='25DISGCVCMZOO2PKP4HOG3QUKC05MHIVFQEUH1HQUQ2OMJXT', client_secret='JLVANPHZENG3QWOLSBRF4BIMJKWNPY343GWQRMIQIWGGISCJ')
        self.api_name = 'Foursquare'

    def _prepare_request(self, lod, context=None):
        if lod.lat:
            lat = lod.lat
        elif context and context.lat:
            lat = context.lat
        else:
            lat = None
        if lod.lng:
            lng = lod.lng
        elif context and context.lng:
            lng = context.lng
        else:
            lng = None
        # prepare request
        q = ''
        if context:
            q = context.label
        if lod and (not lod.lat):
            q = lod.label
        return q, lat, lng

    def invoke(self, lod, context=None):
        """Invoke Foursquare API with a LOD resource and a context.

        Args:
            lod (object): instance of linkeddata.LinkedData

            context (object): instance of linkeddata.LinkedData

        Returns:
            (list): a list of images
        """
        q, lat, lng = self._prepare_request(lod, context)
        image_list = []
        for venue in self.api.venues.search(params={'query': q, 'll': lat + ',' + lng})['venues']:
            try:
                for photo in self.api.venues.photos(venue['id'], {'group': 'venue'})['photos']['items']:
                    image = model.Image()
                    image.source = 'Foursquare'
                    image.title = venue['name']
                    image.published = datetime.fromtimestamp(int(photo['createdAt']))
                    image.width = photo['width']
                    image.height = photo['height']
                    image.author_name = photo['user']['firstName'] + ' ' + photo['user']['lastName']
                    image.author_uri = 'https://foursquare.com/user/' + photo['user']['id']
                    image.locator = photo['prefix'] + 'original' + photo['suffix']
                    image.query_lod = lod.uri
                    if context:
                        image.query_context = context.uri
                    image_list.append(image)
            except Exception as e:
                logger = logging.getLogger('error')
                logger.error('Error in invoking Foursquare API: ' + str(e))
        return image_list

    def loop_invoke(self, lod, context):
        """Iteratively invoke Foursquare API with a LOD resource and a context, and save the results into ElasticSearch.

        Args:
            lod (object): instance of linkeddata.LinkedData

            context (object): instance of linkeddata.LinkedData
        """
        try:
            media_resources = self.invoke(lod, context)
            # add to elasticsearch
            elastic_search_client = esclient.ElasticSearchClient(config.elastic_search_endpoint)
            for m in media_resources:
                if not elastic_search_client.find_media_by_locator(m.locator):
                    if isinstance(m, model.VideoTrack):
                        elastic_search_client.index_video(json.dumps(m, cls=model.VideoEncoder))
                    elif isinstance(m, model.Image):
                        elastic_search_client.index_image(json.dumps(m, cls=model.ImageEncoder))
        except Exception as e:
            logger = logging.getLogger('error')
            logger.error('Error in invoking Foursquare API: ' + str(e))


def invoke(lod_uri, context_uri=None, limit=None, ner=True, media_type='all'):
    """Invoke all of the suitable APIs with a LOD resource and a context in a multi-threading way.

    Args:
        lod_uri (str): URI of LOD resource

        context_uri (str): URI of context

        limit (integer): total number of media resources

        ner (bool): enrich the metadata of resulting media resources or not

        media_type (str): it can be 'all', 'video' or 'image'

    Returns:
        (list): list of media resources
    """
    lod_data = LinkedData(lod_uri)
    if context_uri:
        context_data = LinkedData(context_uri)
    else:
        context_data = None
    global media_list, mutex
    threads = []
    media_list = []
    mutex = threading.Lock()
    if media_type.lower() == 'video' or media_type.lower() == 'all':
        threads.append(threading.Thread(target=thread_invoking, args=(YouTubeAPI(), lod_data, context_data)))
    if media_type.lower() == 'image' or media_type.lower() == 'all':
        threads.append(threading.Thread(target=thread_invoking, args=(FlickrAPI(), lod_data, context_data)))
        threads.append(threading.Thread(target=thread_invoking, args=(InstagramAPIWrapper(), lod_data, context_data)))
        threads.append(threading.Thread(target=thread_invoking, args=(OokabooAPI(), lod_data, context_data)))
        threads.append(threading.Thread(target=thread_invoking, args=(FoursquareAPI(), lod_data, context_data)))
    for t in threads:
        t.start()
    for t in threads:
        t.join(10)
    # apply limit
    if limit:
        video_list = [video for video in media_list if isinstance(video, model.VideoTrack)]
        image_list = [image for image in media_list if isinstance(image, model.Image)]
        if media_type.lower() == 'all':
            video_num = (int(limit) / 2) if (int(limit) / 2) < len(video_list) else len(video_list)
            image_num = limit - video_num
        if media_type.lower() == 'video':
            video_num = int(limit)
            image_num = 0
        if media_type.lower() == 'image':
            video_num = 0
            image_num = int(limit)
        media_list = video_list[0:video_num] + image_list[0:image_num]
    # enrich metadata
    if ner:
        return ner_service.enrich(media_list)
    else:
        return media_list


def thread_invoking(api, lod_data, context_data):
    """Invoke a Web API with a LOD resource and a context in a separate thread, and append results into a global list.

    Args:
        lod_data (object): instance of linkeddata.LinkedData

        context_data (object): instance of linkeddata.LinkedData
    """
    global media_list, mutex
    print api.api_name + ' starts'
    try:
        media_resource = api.invoke(lod_data, context_data)
        mutex.acquire()
        if media_resource:
            media_list += media_resource
        mutex.release()
    except Exception as e:
        logger = logging.getLogger('error')
        logger.error('Error in invoking ' + api.api_name + ' API: ' + str(e))
    print api.api_name + ' ends'


def query_then_invoke(lod_uri, context_uri=None, limit=None, ner=True, media_type='all'):
    """Query ElasticSearch then invoke all of the suitable APIs with a LOD resource and a context.

    Args:
        lod_uri (str): URI of LOD resource

        context_uri (str): URI of context

        limit (integer): total number of media resources

        ner (bool): enrich the metadata of resulting media resources or not

        media_type (str): it can be 'all', 'video' or 'image'

    Returns:
        (list): list of media resources
    """
    # logger = logging.getLogger('webapi')
    try:
        elastic_search_client = esclient.ElasticSearchClient(config.elastic_search_endpoint)
        media_resources = elastic_search_client.query_by_keywords(lod_uri, context_uri, limit, media_type)
    except socket.error:
        media_resources = []
    if (limit and len(media_resources) >= limit) or (limit is None):
        # logger.debug(str(len(media_resources)) + ' is larger than limit')
        return media_resources
    else:
        # contextual query
        try:
            media_resources = contextual_query(lod_uri, context_uri, limit=limit, media_type=media_type)
        except:
            pass
        if len(media_resources) >= limit:
            return media_resources
        else:
            return _merge_media_lists(media_resources, invoke(lod_uri, context_uri, limit - len(media_resources), ner, media_type))


def _expand_query(lod_uri, context_uri):
    context_lod = LinkedData(context_uri)
    queries = []
    for related_concept in context_lod.find_related():
        queries.append((lod_uri, related_concept))
    return queries


@timeout(12)
def contextual_query(lod_uri, context_uri, limit, media_type='all', elastic_search_endpoint=None):
#     logger = logging.getLogger('webapi')
#     logger.debug('start contextual query')
    media_resources = []
    if not context_uri:
        return media_resources
    if elastic_search_endpoint:
        elastic_search_client = esclient.ElasticSearchClient(elastic_search_endpoint)
    else:
        elastic_search_client = esclient.ElasticSearchClient(config.elastic_search_endpoint)
    # contextual query
    queries = _expand_query(lod_uri, context_uri)
    for q in queries:
        related_media = elastic_search_client.query_by_keywords(q[0], q[1], media_type=media_type)
#         print q[0], q[1], len(related_media)
        if len(related_media) > 0:
            media_resources = _merge_media_lists(media_resources, related_media)
        if len(media_resources) >= limit:
            break
    return media_resources


def _is_in_media_list(media, media_list):
    for m in media_list:
        if m.locator == media.locator:
            return True
    return False


def _merge_media_lists(media_list1, media_list2):
    return media_list1 + [m for m in media_list2 if not _is_in_media_list(m, media_list1)]
