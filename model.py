# -*- coding: UTF-8 -*-
"""Class definitions of media resources shared across all the modules within PyLSI.

.. moduleauthor:: Dong Liu <liu.dong66@gmail.com>
"""
import json
from datetime import datetime


class MediaResource(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.locator = None
        self.keywords = []
        self.source = None
        self.query_lod = None
        self.query_context = None
        self.created = None
        self.author_name = None
        self.author_uri = None
        self.width = None
        self.height = None
        self.latitude = None
        self.longitude = None
        self.location_name = None
        self.published = None
        # 'crawled', 'enriched'
        self.status = 'crawled'


class VideoTrack(MediaResource):
    def __init__(self):
        super(VideoTrack, self).__init__()
        self.type = 'video'
        self.thumbnail = None
        self.duration = None


class Image(MediaResource):
    def __init__(self):
        super(Image, self).__init__()
        self.type = 'image'


class VideoEncoder(json.JSONEncoder):
    """The JSON encoder for video tracks."""
    def default(self, obj):
        if isinstance(obj, VideoTrack):
            prop_dict = obj.__dict__.copy()
            del prop_dict['id']
            return prop_dict
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        else:
            return json.JSONEncoder.default(self, obj)


class ImageEncoder(json.JSONEncoder):
    """The JSON encoder for images."""
    def default(self, obj):
        if isinstance(obj, Image):
            prop_dict = obj.__dict__.copy()
            del prop_dict['id']
            return prop_dict
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        else:
            return json.JSONEncoder.default(self, obj)
