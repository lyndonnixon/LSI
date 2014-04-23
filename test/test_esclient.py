'''
@author: liud01
'''
import unittest
import esclient

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

#     def testIndexVideo(self):
#         elastic_search_client = esclient.ElasticSearchClient('http://127.0.0.1:9200')
#         self.assertIsNotNone(elastic_search_client)
#         video_data = '{"status": "crawled", "description": null, "title": "Art of Brass Vienna plays Contrapunctus 9 by Johann Sebastian Bach", "type": "video", "created": "2012-12-17T12:50:11.000Z", "source": "YouTube", "query_lod": "http://dbpedia.org/resource/Vienna", "keywords": [], "duration": "197", "locator": "https://www.youtube.com/watch?v=INHAtBuy13w&feature=youtube_gdata_player", "thumbnail": "http://i.ytimg.com/vi/INHAtBuy13w/default.jpg", "query_context": "http://dbpedia.org/resource/Johann_Sebastian_Bach"}'
#         indexed_video = elastic_search_client.get_video(elastic_search_client.index_video(video_data))
#         self.assertEqual("Art of Brass Vienna plays Contrapunctus 9 by Johann Sebastian Bach",
#                          indexed_video.title)

#     def testIsCrawled(self):
#         elastic_search_client = esclient.ElasticSearchClient('http://127.0.0.1:9200')
#         elastic_search_client.is_crawled('http://dbpedia.org/resource/Vienna', None)
#         elastic_search_client.is_crawled('http://dbpedia.org/resource/Vienna', 'http://dbpedia.org/resource/Johann_Sebastian_Bach')

    def testQueryByKeywords(self):
        elastic_search_client = esclient.ElasticSearchClient('http://production.sti2.org:9200')
        media_list = elastic_search_client.query_by_keywords(lod_uri='http://dbpedia.org/resource/Schladming',
                                                             context_uri=None, limit=10)
        for m in media_list:
            print m.title
            print m.locator

#     def testCountVideo(self):
#         elastic_search_client = esclient.ElasticSearchClient('http://127.0.0.1:9200')
#         print elastic_search_client.count_video('http://dbpedia.org/resource/Schladming', None)
#         print elastic_search_client.count_image('http://dbpedia.org/resource/Schladming', None)

if __name__ == "__main__":
    unittest.main()
