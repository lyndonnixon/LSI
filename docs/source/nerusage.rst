Integration with Named Entity Recognition services
==================================================

Introduction
------------

In order to enrich the metadata of media resources, two Named Entity Recognition (NER) services, i.e. `Zemanta API <http://www.zemanta.com/api/>`_ and `NERD API <http://nerd.eurecom.fr/>`_ are integrated into PyLSI. By invoking those two services, named entities, concepts and instances of Linked Data, e.g. people and places, can be automatically recognized from the title and description of a media resource.


Invocation of Zemanta API
-------------------------

To invoke Zemanta API, the title and description of a media resource will be sent to the RESTful endpoint, i.e. http://api.zemanta.com/services/rest/0.0/. For those media resources that do not have descriptions, their titles will be used in the requests.

In more details, the parameters of a request send to Zemanta are as follows (shown as a Python dictionary):

.. code-block:: python

    {"method": "zemanta.suggest",
     "api_key": api_key,
     "text_title": title.encode("utf-8"),
     "text": description.encode("utf-8"),
     "return_images": "0",
     "return_keywords": "0",
     "return_rdf_links": "1",
     "articles_limit": "0",
     "format": "json"}


Invocation of NERD API
-------------------------

NERD API is different from Zemanta. It does not distinguish title from description. Therefore, if a media resource has both title and description, the title and description will be concatenated first, and then be sent to NERD.

The Python codes of invoking NERD API via `NERD4python <https://github.com/giusepperizzo/nerd4python>`_ are as follows.

.. code-block:: python

        n = nerd.NERD('nerd.eurecom.fr', nerd_api_key)
        n.extract(text.encode('utf-8'), 'combined', 3000):


Examples
--------

A YouTube video (https://www.youtube.com/watch?v=I8R1f8d1oLI) titled "Beethoven -9th Symphony 4th Movement- Vienna Philharmonic Part 1" has a description as: "Ludwig van Beethoven Christian Thielemann -conductor- Vienna Philharmonic Orchestra."


The results of invoking Zemanta API are:

.. code-block:: python

    http://rdf.freebase.com/ns/en/vienna_philharmonic_orchestra
    http://dbpedia.org/resource/Vienna_Philharmonic
    http://musicbrainz.org/mm-2.1/artist/d770374d-05e9-4ed3-a068-3fbd4e6e4dd6/4
    http://rdf.freebase.com/ns/en/christian_thielemann
    http://dbpedia.org/resource/Christian_Thielemann
    http://rdf.freebase.com/ns/en/ludwig_van_beethoven
    http://dbpedia.org/resource/Ludwig_van_Beethoven
    http://musicbrainz.org/mm-2.1/artist/1f9df192-a621-4f54-8850-2c5373b7eac9/4


The results of invoking NERD API are:

.. code-block:: python

    http://dbpedia.org/resource/Ludwig_van_Beethoven
    http://dbpedia.org/resource/Symphony_No._9_%28Dvo%C5%99%C3%A1k%29
    http://dbpedia.org/resource/Vienna_Philharmonic
    http://dbpedia.org/resource/Ludwig_van_Beethoven
    http://dbpedia.org/resource/Conducting
    http://dbpedia.org/resource/Vienna_Philharmonic


Known issues
------------

- NERD API has limited support to multi-languages such as German
