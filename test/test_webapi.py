'''
Created on Apr 20, 2013

@author: liud01
'''
import unittest
from linkeddata import LinkedData
from webapi import YouTubeAPI, FlickrAPI, FoursquareAPI, OokabooAPI
from webapi import InstagramAPIWrapper as InstagramAPI 
import serializer
import webapi
import pickle
import lsilog
import json
import model
import serializer

class Test(unittest.TestCase):

    def setUp(self):
        self.lod = LinkedData('http://dbpedia.org/resource/Schladming')
        self.context = LinkedData('http://dbpedia.org/resource/Skiing')

    def tearDown(self):
        pass

#     def testPrepareFoursquareRequest(self):
#         foursquare_api = FoursquareAPI()
#         for photo in foursquare_api.invoke(self.lod, self.context):
#             print photo.locator

#     def testPrepareInstagramRequest(self):
#         instagram_api = InstagramAPI()
#         q, lat, lng = instagram_api._prepare_request(self.lod, self.context)
#         self.assertEquals(q, 'Schladming Skiing')
#         self.assertEquals(lat, '47.3941666667')
#         self.assertEquals(lng, '13.6891666667')
#         q, lat, lng = instagram_api._prepare_request(self.context, self.lod)
#         self.assertEquals(q, 'Skiing Schladming')
#         self.assertEquals(lat, '47.3941666667')
#         self.assertEquals(lng, '13.6891666667')
# 
#     def testPrepareFlickrRequest(self):
#         flickr_api = FlickrAPI()
#         request1 = flickr_api._prepare_request(self.lod, self.context)
#         self.assertEquals(request1, 'http://api.flickr.com/services/rest/?method=flickr.photos.search&extras=description,date_upload&api_key=ca46db6f999837f739c431ca0bd2fb33&format=json&nojsoncallback=1&text=Schladming+Skiing&page=1')
#         request2 = flickr_api._prepare_request(self.context, self.lod)
#         self.assertEquals(request2, 'http://api.flickr.com/services/rest/?method=flickr.photos.search&extras=description,date_upload&api_key=ca46db6f999837f739c431ca0bd2fb33&format=json&nojsoncallback=1&text=Skiing+Schladming&page=1')
# 
#     def testPrepareYouTubeRequest(self):
#         youtube_api = YouTubeAPI()
#         request1 = youtube_api._prepare_request(self.lod, self.context)
#         self.assertEquals(request1, 'https://gdata.youtube.com/feeds/api/videos?q=Schladming+Skiing&start-index=1&max-results=20&v=2')
#         request2 = youtube_api._prepare_request(self.context, self.lod)
#         self.assertEquals(request2, 'https://gdata.youtube.com/feeds/api/videos?q=Skiing+Schladming&start-index=1&max-results=20&v=2')

#     def testInvokeWebAPIs(self):
#         media_list = []
#         ookaboo_api = OokabooAPI()
#         media_list += ookaboo_api.invoke(LinkedData('http://dbpedia.org/resource/Vienna'), self.context)
#         youtube_api = YouTubeAPI()
#         media_list += youtube_api.invoke(LinkedData('http://de.dbpedia.org/resource/Salzkammergut'), None)
#         media_list += youtube_api.invoke(self.lod, self.context)
#         flickr_api = FlickrAPI()
#         media_list += flickr_api.invoke(LinkedData('http://de.dbpedia.org/resource/Salzkammergut'), None)
#         media_list += flickr_api.invoke(self.lod, self.context)
#         instagram_api = InstagramAPI()
#         media_list += instagram_api.invoke(LinkedData('http://de.dbpedia.org/resource/Salzkammergut'), None)
#         media_list += instagram_api.invoke(LinkedData('http://dbpedia.org/resource/Vienna'), self.context)
#         foursquare_api = FoursquareAPI()
#         media_list += foursquare_api.invoke(LinkedData('http://dbpedia.org/resource/Vienna'), self.context)
#         for m in media_list:
#             print json.dumps(m, cls=model.VideoEncoder)
#         print serializer.serialize_as_rdf(media_list)

#     def testThreadingInvokeWebAPIs(self):
#         media_list = webapi.invoke('http://dbpedia.org/resource/Vienna', 'http://dbpedia.org/resource/Skiing', 10)
#         print serializer.serialize_as_rdf(media_list)
#         pickle.dump(media_list, open("media_list.p", "wb"))

#     def testLoopInvokerFlickr(self):
#         flickr_api = FlickrAPI()
#         for m in flickr_api.loop_invoke(LinkedData('http://dbpedia.org/resource/Vienna'), self.context):
#             print m.locator

#     def testLoopInvokerInstagram(self):
#         instagram_api = InstagramAPI()
#         for m in instagram_api.loop_invoke(LinkedData('http://de.dbpedia.org/resource/Salzkammergut'), None):
#             print m.locator

#     def testLoopInvokeOokaoo(self):
#         ookaboo_api = OokabooAPI()
#         media_list = ookaboo_api.loop_invoke(LinkedData('http://dbpedia.org/resource/Vienna'), None)
#         for m in media_list:
#             self.assertIsNotNone(m.height)
#             self.assertIsNotNone(m.width)
#         print serializer.serialize_as_rdf(media_list)

#     def testLoopInvokeYoutube(self):
#         youtube_api = YouTubeAPI()
#         youtube_api.loop_invoke(LinkedData('http://dbpedia.org/resource/Vienna'), None)

#     def testQueryThenInovke(self):
#         lsilog.init_logging_sys()
#         for m in webapi.query_then_invoke('http://de.dbpedia.org/resource/Salzkammergut', None, 10):
#             print m.locator
#         media_list = webapi.query_then_invoke(lod_uri='http://dbpedia.org/resource/Vienna',
#                                               context_uri='http://dbpedia.org/resource/Johann_Sebastian_Bach',
#                                               context_uri='http://dbpedia.org/resource/Johann_Sebastian_Bach',
#                                               limit=10, media_type='all')
#         print serializer.serialize_as_rdf(media_list)
#         for m in media_list:
#             print m.locator
#             if hasattr(m, 'created') and m.created:
#                 print m.created

#     def testExpandQuery(self):
#         queries = webapi._expand_query('http://dbpedia.org/resource/Kart_Racing', 'http://dbpedia.org/resource/Schladming')
#         self.assertIn(('http://dbpedia.org/resource/Kart_Racing', 'http://dbpedia.org/resource/Donauradweg'), queries)
#         self.assertIn(('http://dbpedia.org/resource/Kart_Racing', 'http://dbpedia.org/resource/Obertauern'), queries)
#         self.assertIn(('http://dbpedia.org/resource/Kart_Racing', 'http://dbpedia.org/resource/Hochfilzen'), queries)
#         self.assertIn(('http://dbpedia.org/resource/Kart_Racing', 'http://dbpedia.org/resource/Mayrhofen'), queries)

#     def testContextualQuery(self):
#         meida_list = webapi.contextual_query(lod_uri='http://dbpedia.org/resource/Vienna',
#                                 context_uri='http://dbpedia.org/resource/Johannes_Bach',
#                                 limit=10, elastic_search_endpoint='http://production.sti2.org:9200')
#         print meida_list

    def testReturnOnlyOneVideo(self):
#         lod = LinkedData("http://dbpedia.org/resource/Barack_Obama")
#         context = LinkedData("http://dbpedia.org/resource/Washington_DC")
#         youtube_api = webapi.YouTubeAPI()
#         print len(youtube_api.invoke(lod=lod, context=context))
        for m in webapi.query_then_invoke(lod_uri="http://dbpedia.org/resource/Barack_Obama",
                                          context_uri="http://dbpedia.org/resource/Washington_DC",
                                          limit=3, media_type="video"):
            print m.locator

if __name__ == "__main__":
    unittest.main()
