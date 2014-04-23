#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Periodically enrich the metadata of media resources by invoking Named Entity Recognition Services.

.. moduleauthor:: Dong Liu <liu.dong66@gmail.com>
"""
import config
import esclient
import ner
import model
import json
import logging
import lsilog
from time import sleep


def enrich(media_count):
    """Enrich the metadata of a number of media resources.

    Args:
        media_count (int): The number of the media resources to be enriched.
    """
    elastic_search_client = esclient.ElasticSearchClient(config.elastic_search_endpoint)
    enriched_count = 0
    enriched_video = 0
    enriched_image = 0
    while True:
        if enriched_count >= media_count:
            break
        media_list = elastic_search_client.find_media_by_status('crawled')
        for media in ner.enrich(media_list, keep_ner_log=True):
            media.status = 'enriched'
            sleep(1)
            if isinstance(media, model.VideoTrack):
                enriched_video += 1
                elastic_search_client.update_video(media.id, json.dumps(media, cls=model.VideoEncoder))
            elif isinstance(media, model.Image):
                enriched_image += 1
                elastic_search_client.update_image(media.id, json.dumps(media, cls=model.ImageEncoder))
            enriched_count += 1
    logger = logging.getLogger("enricher")
    logger.info('Enriched ' + str(enriched_count) + ' meida resources: ' + str(enriched_video) + ' videos and ' + str(enriched_image) + ' images')

if __name__ == '__main__':
    lsilog.init_logging_sys()
    enrich(1500)
    logging.shutdown()
