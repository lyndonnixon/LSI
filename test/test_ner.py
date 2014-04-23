'''
Created on Apr 21, 2013

@author: liud01
'''
import unittest
import pickle
import ner
import serializer


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testThreadingEnriching(self):
        media_list = pickle.load(open("resources/media_list.p", "rb"))
        enriched_media_list = ner.enrich(media_list)
        for m in enriched_media_list:
            print m.keywords
        print serializer.serialize_as_rdf(enriched_media_list)

if __name__ == "__main__":
    unittest.main()
