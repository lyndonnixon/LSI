'''
Created on Apr 20, 2013

@author: liud01
'''
import web
import webapi
import serializer


class Invoke(object):

    def GET(self):
        if 'lod' in web.input():
            lod = web.input().lod
        if 'context' in web.input():
            context = web.input().context
        else:
            context = None
        if 'limit' in web.input():
            limit = int(web.input().limit)
        else:
            limit = 10
        if 'mediaType' in web.input():
            media_type = web.input().mediaType.lower()
        else:
            media_type = 'all'
        media_list = webapi.query_then_invoke(lod, context, limit, media_type=media_type)
        web.header('Content-Type', 'application/rdf+xml')
        return serializer.serialize_as_rdf(media_list)
