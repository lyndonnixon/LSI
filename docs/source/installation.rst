Installation
============

.. contents::
    :local:
    :depth: 2

Install Python Packages
-----------------------

To get PyLSI running, please make sure that you are using Python 2.7.3. The following Python packages need to be installed using pip::

    pip install web.py
    pip install RDFAlchemy
    pip install httplib2
    pip install lxml
    pip install python-dateutil
    pip install python-instagram
    pip install foursquare
    pip install gdata
    pip install chardet
    pip install openpyxl

Install ElasticSearch
---------------------

Please follow the guide to set up ElasticSearch: http://www.elasticsearch.org/guide/reference/setup/, and run es-init.sh to initialize the ElasticSearch indexes for PyLSI.


Install PyLSI
-------------

Modify the config file (i.e. config.py) to set the endpoint of the ElasticSearch server. And then, you can go to the folder of pylsi and run::

    python webapp.py

If you have got `uwsgi <https://github.com/unbit/uwsgi-docs>`_ installed, you can run:

.. code-block:: bash

    sudo uwsgi uwsgi.ini

The installation of PyLSI has been done. Now, you can browse to http://localhost:8080/lsi or http://localhost/lsi (for the one running with uwsgi).


Appendix: Links to Dependencies
-------------------------------

- web.py: http://webpy.org/
- RDFAlchemy: http://www.openvest.com/trac/wiki/RDFAlchemy
- httplib2: https://code.google.com/p/httplib2/
- lxml: http://lxml.de/
- chardet: https://pypi.python.org/pypi/chardet
- openpyxl: http://pythonhosted.org/openpyxl/
- python-instagram: https://github.com/Instagram/python-instagram
- foursquare: https://github.com/mLewisLogic/foursquare
- gdata: https://code.google.com/p/gdata-python-client/
- python-dateutil: https://pypi.python.org/pypi/python-dateutil
