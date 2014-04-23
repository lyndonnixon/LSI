# -*- coding: UTF-8 -*-
"""Collect Linked Data and find related Linked Data.

.. moduleauthor:: Dong Liu <liu.dong66@gmail.com>
"""
from urlparse import urlparse
from rdflib.graph import Graph
from rdfalchemy.sparql import SPARQLGraph
from rdflib import Namespace
from rdflib import URIRef
from rdflib import RDFS
import utils
from utils import timeout
from utils import TimeoutException
import urllib


class LinkedDataSourceUnreachable(Exception):
    pass


class LinkedData(object):
    """Linked Data collector.

    The actual RDF data will be retrieved during instantiation.
    """
    def __init__(self, uri):
        """Initialize and retrieve Linked Data on the Web."""
        self.uri = self._encode_lod_uri(uri)
        self.label = None
        self.lat = None
        self.lng = None
        if uri:
            self.uri_ref = URIRef(uri)
            try:
                self._get_values(self._find_graph())
            except TimeoutException:
                raise LinkedDataSourceUnreachable(self.uri)

    def _encode_lod_uri(self, uri):
#         parse uri
        o = urlparse(uri)
        scheme = o.scheme
        netloc = o.netloc
        path = o.path
        params = o.params
        query = o.query
        fragment = o.fragment
        encoded_uri = str(scheme) + '://' + str(netloc)
        # urlencode path
        if path:
            path_tokens = []
            for t in path.split('/'):
                t = urllib.quote(t.encode('utf-8'))
                path_tokens.append(t)
            encoded_uri += '/'.join(path_tokens)
        if params:
            encoded_uri += ';' + str(params)
        if query:
            encoded_uri += '?' + str(query)
        if fragment:
            encoded_uri += '#' + str(fragment)
        return encoded_uri

    def _find_graph(self):
        if self._is_dbpedia_uri():
            return SPARQLGraph('http://dbpedia.org/sparql')
        else:
            graph = Graph()
            graph.parse(self.uri)
            return graph

    @timeout(5)
    def _get_values(self, graph):
        # sleep(10)
        label_en = None
        label_de = None
        for label in graph.objects(subject=self.uri_ref, predicate=RDFS.label):
            if not self.label:
                self.label = utils.smartcode(label)
            if label.language == 'en':
                label_en = utils.smartcode(label)
            elif label.language == 'de':
                label_de = utils.smartcode(label)
        if label_en:
            self.label = label_en
        elif label_de:
            self.label = label_de
        geo = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
        dbpprop = Namespace('http://dbpedia.org/property/')
        self.lat = None
        self.lng = None
        try:
            self.lat = str(graph.objects(subject=self.uri_ref, predicate=geo.lat).next())
        except:
            pass
        try:
            self.lng = str(graph.objects(subject=self.uri_ref, predicate=geo.long).next())
        except:
            pass
        try:
            lat_deg = int(graph.objects(subject=self.uri_ref, predicate=dbpprop.latDeg).next())
            lat_min = int(graph.objects(subject=self.uri_ref, predicate=dbpprop.latMin).next())
            lat_sec = int(graph.objects(subject=self.uri_ref, predicate=dbpprop.latSec).next())
            self.lat = str(lat_deg + float(lat_min)/60 + float(lat_sec)/3600)
        except:
            pass
        try:
            lng_deg = int(graph.objects(subject=self.uri_ref, predicate=dbpprop.lonDeg).next())
            lng_min = int(graph.objects(subject=self.uri_ref, predicate=dbpprop.lonMin).next())
            lng_sec = int(graph.objects(subject=self.uri_ref, predicate=dbpprop.lonSec).next())
            self.lng = str(lng_deg + float(lng_min)/60 + float(lng_sec)/3600)
        except:
            pass

    def _is_dbpedia_uri(self):
        o = urlparse(self.uri)
        if o.netloc.lower() == 'dbpedia.org' and o.path.startswith('/resource/'):
            return True
        else:
            return False

    def find_related(self):
        """Find related Linked Data.

        Returns:
            A list of the URIs of the related Linked Data.
        """
        related_concepts = []
        if not self._is_dbpedia_uri():
            return related_concepts
        graph = SPARQLGraph('http://dbpedia.org/sparql')
#         query = '''
#                 PREFIX dcterms: <http://purl.org/dc/terms/>
#                 PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
#                 SELECT DISTINCT ?c WHERE {
#                     {
#                         <%s> dcterms:subject ?cat .
#                         ?c dcterms:subject ?cat .
#                     } UNION {
#                         <%s> dcterms:subject ?cat .
#                         ?n_cat skos:broader ?cat .
#                         ?c dcterms:subject ?n_cat .
#                     } UNION {
#                         <%s> dcterms:subject ?cat .
#                         ?cat skos:broader ?n_cat .
#                         ?c dcterms:subject ?n_cat .
#                     }
#                 }'''
#         query = query % (self.uri, self.uri, self.uri)
        query = '''
                PREFIX dcterms: <http://purl.org/dc/terms/>
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                SELECT DISTINCT ?c WHERE {
                    {
                        <%s> dcterms:subject ?cat .
                        ?c dcterms:subject ?cat .
                    }
                }'''
        query = query % self.uri
#         i = 0
        for r in graph.query(query, resultMethod='json'):
#             if i > 10:
#                 break
            if str(r[0]) != self.uri:
                related_concepts.append(str(r[0]))
#                 i += 1
        return related_concepts
