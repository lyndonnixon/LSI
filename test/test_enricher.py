'''
Created on Apr 21, 2013

@author: liud01
'''
import unittest
import enricher


class Test(unittest.TestCase):

    def testEnrich(self):
        enricher.enrich(15)

if __name__ == "__main__":
    unittest.main()
