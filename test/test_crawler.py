'''
Created on Apr 21, 2013

@author: liud01
'''
import unittest
import crawler


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCrawl(self):
        crawler.crawl('http://dbpedia.org/resource/Vienna', None)
#         crawler.crawl('http://dbpedia.org/resource/Vienna',
#                       'http://dbpedia.org/resource/Johann_Sebastian_Bach')

    def testParseConfigFile(self):
        for q in crawler._parse_queries_file('/Users/liud01/Dropbox/root/workspace/python/pylsi/queries.json'):
            print q

if __name__ == "__main__":
    unittest.main()
