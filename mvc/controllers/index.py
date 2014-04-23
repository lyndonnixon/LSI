# -*- coding: UTF-8 -*-

from webapp import html_render

class Index(object):

    def GET(self):
        return html_render.index()
