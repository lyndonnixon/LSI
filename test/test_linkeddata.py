# -*- coding: UTF-8 -*-
'''
Created on Apr 20, 2013

@author: liud01
'''
import unittest
from linkeddata import LinkedData
import linkeddata


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

#     def testCollectLinkedData(self):
#         lod = LinkedData('http://dbpedia.org/resource/Vienna')
#         self.assertEquals(lod.label, 'Vienna')
#         self.assertTrue(lod.lat.startswith('48.20'))
#         self.assertTrue(lod.lng.startswith('16.37'))
#         lod = LinkedData('http://de.dbpedia.org/resource/Vienna')
#         self.assertEquals(lod.label, 'Vienna')
#         lod = LinkedData('http://dbpedia.org/resource/Schladming')
#         self.assertEquals(lod.label, 'Schladming')
#         lod = LinkedData('http://dbpedia.org/resource/London')
#         self.assertEquals(lod.label, 'London')
#         self.assertTrue(lod.lat.startswith('51.50'))
#         lod = LinkedData('http://dbpedia.org/resource/Johann_Sebastian_Bach')
#         self.assertEquals(lod.label, 'Johann Sebastian Bach')
#         lod = LinkedData('http://dbpedia.org/resource/Skiing')
#         self.assertEquals(lod.label, 'Skiing')
#         lod = LinkedData('http://dbpedia.org/resource/Schladming')
#         self.assertTrue(lod.lat.startswith('47.39'))
#         self.assertTrue(lod.lng.startswith('13.68'))
#         lod = LinkedData('http://de.dbpedia.org/resource/Salzkammergut')
#         self.assertEquals(lod.label, 'Salzkammergut')
#         print lod.lat
#         print lod.lng

#     def testIsDBpediaURI(self):
#         lod = LinkedData('http://dbpedia.org/resource/Vienna')
#         self.assertTrue(lod._is_dbpedia_uri())

    def testFindRelatedConcepts(self):
#         lod = LinkedData('http://dbpedia.org/resource/Schladming')
#         related_lod_resources = lod.find_related()
#         self.assertIn('http://dbpedia.org/resource/Obertauern', related_lod_resources)
#         self.assertIn('http://dbpedia.org/resource/Hochfilzen', related_lod_resources)
#         self.assertIn('http://dbpedia.org/resource/Mayrhofen', related_lod_resources)
#         self.assertIn('http://dbpedia.org/resource/S%C3%B6lden', related_lod_resources)
        lod = LinkedData('http://dbpedia.org/resource/Johannes_Bach')
        related_lod_resources = lod.find_related()
        for r in related_lod_resources:
            print r
#         print len(related_lod_resources)
#         print related_lod_resources

#     def testEncodingProblem(self):
#         lod = LinkedData('http://dbpedia.org/resource/London')
#         self.assertEquals(lod.uri, 'http://dbpedia.org/resource/London')
#         lod = LinkedData('http://dbpedia.org/resource/Luis_Buñuel')
#         self.assertEquals(lod.uri, 'http://dbpedia.org/resource/Luis_Bu%C3%B1uel')

if __name__ == "__main__":
    unittest.main()
