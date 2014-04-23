#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""Endpoint of the Web interface of PyLSI

Args:
    urls (dict): URL mappings.

    html_render (object): HTML page render.

    app (object): instance of Web.py Web application.

    application (object): WSGI interface of the Web application

.. moduleauthor:: Dong Liu <liu.dong66@gmail.com>
"""
import web

urls = (
    '/lsi', 'mvc.controllers.index.Index',
    '/lsi/', 'mvc.controllers.index.Index',
    '/lsi/search', 'mvc.controllers.search.Search',
    '/lsi/api/invoke', 'mvc.controllers.api.Invoke')

web.config.debug = True

html_render = web.template.render('mvc/views/')

app = web.application(urls, globals())

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
