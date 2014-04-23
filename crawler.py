#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Periodically collect media resources by invoking the Web APIs, and save them into ElasticSearch.

.. moduleauthor:: Dong Liu <liu.dong66@gmail.com>
"""
from linkeddata import LinkedData
from webapi import YouTubeAPI, FlickrAPI, InstagramAPIWrapper, OokabooAPI,\
    FoursquareAPI
import threading
import esclient
import config
import json
import lsilog
import logging
from time import sleep


def _thread_crawling(api, lod_data, context_data):
    logger = logging.getLogger('crawler')
    logger.debug('Thread start ' + api.api_name + " " + lod_data.uri + " " + str(context_data))
    api.loop_invoke(lod_data, context_data)
    logger.debug('Thread end ' + api.api_name + " " + lod_data.uri + " " + str(context_data))


def _parse_queries_file(path='queries.json'):
    """Parse the queries.json file, return a list of JSON objects

    Kwargs:
        path (str): Path to the queries.json file (default: ./queries.json).
    """
    queries_file = open(path)
    queries = json.load(queries_file)['queries']
    queries_file.close()
    return queries


def crawl(lod_uri, context_uri):
    """Crawl videos and images by invoking Web APIs.

    Args:
        lod_uri (str): The URI of Linked Open Data.

        context_uri (str): The URI of Linked Open Data used as the context.
    """
    lod_data = LinkedData(lod_uri)
    if context_uri:
        context_data = LinkedData(context_uri)
    else:
        context_data = None
    threads = []
    threads.append(threading.Thread(target=_thread_crawling, args=(YouTubeAPI(), lod_data, context_data)))
    threads.append(threading.Thread(target=_thread_crawling, args=(FlickrAPI(), lod_data, context_data)))
    threads.append(threading.Thread(target=_thread_crawling, args=(InstagramAPIWrapper(), lod_data, context_data)))
    threads.append(threading.Thread(target=_thread_crawling, args=(OokabooAPI(), lod_data, context_data)))
    threads.append(threading.Thread(target=_thread_crawling, args=(FoursquareAPI(), lod_data, context_data)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def batch_crawl(queries_file='queries.json'):
    """Crawl videos and images by invoking Web APIs with a batch of queries.

    Kwargs:
        queries_file (str): Path to the queries.json file (default: ./queries.json).

    Sample of the queries file:

    .. code-block:: json

        {"queries": [{
                "lod_uri": "http://dbpedia.org/resource/Vienna",
                "context": "http://dbpedia.org/resource/Johann_Sebastian_Bach"
            }]
        }
    """
    logger = logging.getLogger('crawler')
    for query in _parse_queries_file(queries_file):
        lod_uri = query['lod_uri']
        try:
            context_uri = query['context']
        except:
            context_uri = None
        logger.debug('Start crawling: ' + lod_uri + ' ' + str(context_uri))
        crawl(lod_uri, context_uri)
        logger.debug('Finish crawling: ' + lod_uri + ' ' + str(context_uri))
        sleep(2)
        logger.debug('Writing crawling logs')
        elastic_search_client = esclient.ElasticSearchClient(config.elastic_search_endpoint)
        video_count = elastic_search_client.count_video(lod_uri, context_uri)
        image_count = elastic_search_client.count_image(lod_uri, context_uri)
        logger.info(' -- '.join((lod_uri, str(context_uri), str(video_count), str(image_count))))

if __name__ == '__main__':
    lsilog.init_logging_sys()
    batch_crawl()
    logging.shutdown()
