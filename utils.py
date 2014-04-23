# -*- coding: UTF-8 -*-
"""Utilities of LSI

.. moduleauthor:: Dong Liu <liu.dong66@gmail.com>
"""
import chardet
import threading
import sys


class TimeoutException(Exception):
    pass


def smartcode(ostring):
    """Transform the original string into a UTF-8 string

    Args:
        ostring (str): the original string.
    """
    try:
        codedetect = chardet.detect(ostring)["encoding"]
        return unicode(ostring, codedetect).encode('utf-8')
    except:
        return ostring.encode('utf-8')


def timeout(timeout_time):
    """A decorator for setting up time out for a function

    Args:
        timeout_time (int): time out in secondes.

    Throws:
        TimeoutException
    """
    def internal(function):
        def internal2(*args, **kw):
            class Calculator(threading.Thread):
                def __init__(self):
                    threading.Thread.__init__(self)
                    self.result = None
                    self.error = None

                def run(self):
                    try:
                        self.result = function(*args, **kw)
                    except:
                        self.error = sys.exc_info()[0]
            c = Calculator()
            c.start()
            c.join(timeout_time)
            if c.isAlive():
                raise TimeoutException
            if c.error:
                raise c.error
            return c.result
        return internal2
    return internal
