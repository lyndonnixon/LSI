# -*- coding: UTF-8 -*-
"""Metadata enricher implemented on top of Named Entity Recognition services.

.. moduleauthor:: Dong Liu <liu.dong66@gmail.com>
"""
import threading
import nerd
import urllib
import urllib2
import json
import nerlogger
from datetime import datetime


class EnricherError(Exception):
    pass


def _enrich_zemanta(title, description):
    gateway = 'http://api.zemanta.com/services/rest/0.0/'
    keywords = []
    if description:
        args = {'method': 'zemanta.suggest',
                'api_key': 'pelex6iltt2gmwp8fwlebfft',
                'text_title': title.encode('utf-8'),
                'text': description.encode('utf-8'),
                'return_images': '0',
                'return_keywords': '0',
                'return_rdf_links': '1',
                'articles_limit': '0',
                'format': 'json'}
    else:
        args = {'method': 'zemanta.suggest',
                'api_key': 'pelex6iltt2gmwp8fwlebfft',
                'text': title.encode('utf-8'),
                'return_images': '0',
                'return_keywords': '0',
                'return_rdf_links': '1',
                'articles_limit': '0',
                'format': 'json'}
    args_enc = urllib.urlencode(args)
    raw_output = urllib2.urlopen(gateway, args_enc).read()
    zemanta_json = json.loads(raw_output)
    if zemanta_json['status'] == 'ok':
        for link in zemanta_json['markup']['links']:
            for target in link['target']:
                if target['type'] == 'rdf':
                    if str(target['url']) != 'null' and str(target['url']) != 'NORDF':
                        if not '?' in str(target['url']):
                            if not str(target['url']).startswith('http://maps.google.com/maps'):
                                keywords.append(target['url'])
    else:
        raise EnricherError(raw_output)
    return keywords


def _enrich_nerd(text, timeout=3000):
    keywords = []
    n = nerd.NERD('nerd.eurecom.fr', 'd8issmac4fvpbberlp79sb61na6037d9')
    for entity in n.extract(text.encode('utf-8'), 'combined', timeout):
        if entity['uri']:
            if str(entity['uri']) != 'null' and str(entity['uri']) != 'NORDF':
                if not '?' in str(entity['uri']):
                    if not str(entity['uri']).startswith('http://maps.google.com/maps'):
                        keywords.append(entity['uri'])
    return keywords


def _enrich_combined(title, description):
    keywords = []
    zemanta_results = []
    nerd_results = []
    try:
        zemanta_results = _enrich_zemanta(title, description)
        keywords += zemanta_results
    except Exception as e:
        print e
    try:
        if description:
            nerd_results = _enrich_nerd(title + ' ' + description)
        else:
            nerd_results = _enrich_nerd(title)
        keywords += nerd_results
    except Exception as e:
        print e
    global mutex, ner_logger
    if ner_logger:
        mutex.acquire()
        ner_logger.log(title, description, ', '.join(zemanta_results), ', '.join(nerd_results))
        mutex.release()
    return keywords


def enrich(media_list, keep_ner_log=False):
    """Enrich the metadata of a list of media resources by invoking Zemanta and NERD services.

    Args:
        media_list (list): the list of media resources

        keep_ner_log (bool): save the NER results as an Excel spreadsheet.

    Returns:
        (list): the list of media resources with enriched metadata
    """
    global enriched_media_list, mutex, ner_logger
    threads = []
    enriched_media_list = []
    mutex = threading.Lock()
    if keep_ner_log:
        ner_logger = nerlogger.NERLogger()
    else:
        ner_logger = None
    for m in media_list:
        threads.append(threading.Thread(target=thread_enriching, args=(m,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join(10)
    if keep_ner_log:
        ner_logger.save('xls/NER Log ' + datetime.now().strftime("%Y-%m-%d") + '.xlsx')
    return enriched_media_list


def thread_enriching(media):
    """Enrich the metadata of a media resource using a separate thread, and append it to a list.

    Args:
        media (object): the media resource
    """
    global enriched_media_list, mutex
    threadname = threading.currentThread().getName()
    print 'Enriching thread ' + threadname + ' starts'
    media.keywords = _enrich_combined(media.title, media.description)
    mutex.acquire()
    enriched_media_list.append(media)
    mutex.release()
    print 'Enriching thread ' + threadname + ' ends'
