'''
Created on Apr 20, 2013

@author: liud01
'''
import web
import serializer
import webapi
from webapp import html_render
import model
from linkeddata import LinkedDataSourceUnreachable


class Search(object):

    def GET(self):
        raise web.seeother('/lsi')

    def POST(self):
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
        try:
            media_list = webapi.query_then_invoke(lod, context, limit, media_type=media_type)
            video_list = [video for video in media_list if isinstance(video, model.VideoTrack)]
            image_list = [image for image in media_list if isinstance(image, model.Image)]
            rdf = serializer.serialize_as_rdf(media_list)
            return html_render.search_result(video_list, image_list, rdf)
        except LinkedDataSourceUnreachable as e:
            return html_render.error_info('<a href="' + str(e) + '" target="_blank">' + str(e) + '</a> is unreachable')
