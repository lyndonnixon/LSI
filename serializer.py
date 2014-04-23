"""RDF Serializer

.. moduleauthor:: Dong Liu <liu.dong66@gmail.com>
"""
from rdflib.graph import Graph
from rdflib import Literal
from rdflib import Namespace
from rdflib import URIRef
from rdflib import RDFS
from rdflib import RDF
from rdflib import XSD
import model
import uuid


publisher_uri_dict = {"Ookaboo": "http://ookaboo.com",
                      "YouTube": "http://www.youtube.com",
                      "Flickr": "http://www.flickr.com",
                      "Instagram": "http://instagram.com",
                      "Foursquare": "https://foursquare.com"
                      }


def serialize_as_rdf(media_resources):
    """Serialize a list of media resources as RDF triples.

    Args:
        media_resources (list): the list of media resources.

    Returns:
        string: RDF/XML serialization of the media resources.
    """
    g = Graph('IOMemory')
    g.bind('ma', URIRef('http://www.w3.org/ns/ma-ont#'))
    g.bind('foaf', URIRef('http://xmlns.com/foaf/0.1/'))
    ma = Namespace('http://www.w3.org/ns/ma-ont#')
    foaf = Namespace('http://xmlns.com/foaf/0.1/')
    for media in media_resources:
        if not media.id:
            media.id = str(uuid.uuid4()).replace("-", "")
        media.uri = URIRef('http://production.sti2.org/lsi/media/' + media.id)
        g.add((media.uri, ma.title, Literal(media.title)))
        if media.description:
            g.add((media.uri, ma.description, Literal(media.description)))
        g.add((media.uri, ma.locator, Literal(media.locator, datatype=XSD.anyURI)))
        if hasattr(media, 'width') and media.width:
            g.add((media.uri, ma.width, Literal(media.width, datatype=XSD.integer)))
        if hasattr(media, 'height') and media.height:
            g.add((media.uri, ma.height, Literal(media.height, datatype=XSD.integer)))
        if hasattr(media, 'author_uri') and media.author_uri:
            author_uri_ref = URIRef(media.author_uri)
            g.add((media.uri, ma.contributor, author_uri_ref))
            g.add((author_uri_ref, RDF.type, ma.Agent))
            if hasattr(media, 'author_name') and media.author_name:
                g.add((author_uri_ref, RDFS.label, Literal(media.author_name)))
        if hasattr(media, 'created') and media.created:
            g.add((media.uri, ma.creationDate, Literal(str(media.created).replace(' ', 'T'), datatype=XSD.dateTime)))
        if hasattr(media, 'published') and media.published:
            g.add((media.uri, ma.releaseDate, Literal(str(media.published).replace(' ', 'T'), datatype=XSD.dateTime)))
        if hasattr(media, 'latitude') and media.latitude:
            g.add((media.uri, ma.locationLatitude, Literal(media.latitude, datatype=XSD.double)))
        if hasattr(media, 'longitude') and media.longitude:
            g.add((media.uri, ma.locationLongitude, Literal(media.longitude, datatype=XSD.double)))
        if hasattr(media, 'location_name') and media.location_name:
            g.add((media.uri, ma.locationName, Literal(media.location_name)))
        for keyword in media.keywords:
            g.add((media.uri, ma.hasKeyword, URIRef(keyword)))
        if isinstance(media, model.VideoTrack):
            g.add((media.uri, RDF.type, ma.MediaResource))
            g.add((media.uri, foaf.thumbnail, URIRef(media.thumbnail)))
            g.add((media.uri, ma.duration, Literal(media.duration, datatype=XSD.integer)))
        elif isinstance(media, model.Image):
            g.add((media.uri, RDF.type, ma.Image))
        try:
            g.add((media.uri, ma.publisher, URIRef(publisher_uri_dict.get(media.source))))
        except:
            pass
    return g.serialize(format='xml')
