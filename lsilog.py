# -*- coding: UTF-8 -*-
"""Initializer of the logger of LSI

.. moduleauthor:: Dong Liu <liu.dong66@gmail.com>
"""
import time
import logging
import logging.config


def _create_logger(name, level=logging.INFO):
    formatter = logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler('logs/' + name + '.log.' + time.strftime('%Y-%m-%d', time.localtime(time.time())))
    fh.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(fh)


def init_logging_sys():
    """Initialize of the logging system of LSI"""
    logging.config.fileConfig("lsilog.conf")
    _create_logger('crawler')
    _create_logger('enricher')
    _create_logger('webapi')
    _create_logger('error', logging.ERROR)
