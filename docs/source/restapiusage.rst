Usage of the RESTful API
========================

PyLSI provides a RESTful API for finding media resources, e.g. images and videos, related to a Linked Open Data (LOD) URI.


Request URL
-----------

http://productioin.sti2.org/lsi/api/invoke


HTTP Method
-----------

GET or POST


Parameters
----------

.. table::

   ===========  ========= ===================================================
      Name        Type                        Example
   ===========  ========= ===================================================
    lod          URI       http://dbpedia.org/resource/Vienna
    mediaType    String    all, video, image
    limit        Integer   10
    ner          Boolean   yes or no
    context      String    http://dbpedia.org/resource/Johann_Sebastian_Bach
   ===========  ========= ===================================================


Supported LOD URIs
------------------

- Instances of dbp:Place use geolocation information. Two properties, i.e. latitude (wgs84:lat) and longitude (wgs84:long), will be used to assemble the actual requests to be sent to the endpoints of services
- All the instances of rdf:resource can be used in a service call using its value of rdfs:label. Note: for multi-lingual labels, LSI will choose the one in English.


Example
-------

**Request:**

http://production.sti2.org/lsi/api/invoke?lod=http://dbpedia.org/resource/Vienna&mediaType=all&limit=10&ner=yes&context=http://dbpedia.org/resource/Johann_Sebastian_Bach

**Response:**

The response will be in the format of RDF and conform to the `W3C Media Ontology <http://www.w3.org/TR/mediaont-10/>`_.

- videos are represented as instances of ma:VideoTrack
- images are instances of ma:Image
- metadata such as title, description, image, and duration of videos are in the response
- ma:keyword is used to link back to the LOD URI used as input

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
        xmlns:mo="http://purl.org/ontology/mo/"
        xmlns:foaf="http://xmlns.com/foaf/0.1/"
        xmlns:ma="http://www.w3.org/ns/ma-ont#"
        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        xmlns:h="http://www.w3.org/1999/xhtml"
        xmlns:dcterms="http://purl.org/dc/terms/">

    <rdf:Description rdf:about="http://images.ookaboo.com/photo/l/Josephinische_Landaufnahme_Vienna_2_l.jpg">
        <rdf:type rdf:resource="http://www.w3.org/ns/ma-ont#Image"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://images.ookaboo.com/photo/l/ABK_2C_Vienna_June_2006_592_2_l.jpg">
        <rdf:type rdf:resource="http://www.w3.org/ns/ma-ont#Image"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/55471fa8-6646-4722-afa8-aa862cbd28a6">
        <rdf:type rdf:resource="http://www.w3.org/ns/ma-ont#VideoTrack"/>
        <ma:title rdf:parseType="Literal">J.S. BACH:  AIR Vienna Philharmonic Women??s Orchestra</ma:title>
        <ma:locator rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">https://www.youtube.com/watch?v=3yIcoPrAgvs</ma:locator>
        <ma:description rdf:parseType="Literal">J.S. BACH: Suite Nr. 3 AIR. Vienna Philharmonic Women??s Orchestra, Conductor Izabella Shareyko, performed at St. Thekla Church, Vienna Wieden.</ma:description>
        <foaf:img rdf:resource="http://i.ytimg.com/vi/3yIcoPrAgvs/0.jpg"/>
        <ma:duration rdf:datatype="http://www.w3.org/2001/XMLSchema#float">346</ma:duration>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/94a8b6b7-1041-4ff9-96cb-f4b402c3a2a7">
        <rdf:type rdf:resource="http://www.w3.org/ns/ma-ont#VideoTrack"/>
        <ma:title rdf:parseType="Literal">J. S. Bach's Ave Maria &amp; Vienna Boys Chorus</ma:title>
        <ma:locator rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">https://www.youtube.com/watch?v=W-tvs0Yoy3I</ma:locator>
        <ma:description rdf:parseType="Literal">J. S. Bach's Ave Maria by The Scottish Chamber Orchestra.</ma:description>
        <foaf:img rdf:resource="http://i.ytimg.com/vi/W-tvs0Yoy3I/0.jpg"/>
        <ma:duration rdf:datatype="http://www.w3.org/2001/XMLSchema#float">284</ma:duration>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/1cd3adf2-4137-47b6-8b1d-4b7b809945f6">
        <rdf:type rdf:resource="http://www.w3.org/ns/ma-ont#VideoTrack"/>
        <ma:title rdf:parseType="Literal">Art of Brass Vienna plays Contrapunctus 9 by Johann Sebastian Bach</ma:title>
        <ma:locator rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">https://www.youtube.com/watch?v=INHAtBuy13w</ma:locator>
        <ma:description rdf:parseType="Literal">Johann Sebastian Bach, Contrapunctus No. 9, Art of Brass Vienna, Heinrich Buckner, Hans Gansch, Thomas Bieber, Erich Kojeder, Jonathan Sass.</ma:description>
        <foaf:img rdf:resource="http://i.ytimg.com/vi/INHAtBuy13w/0.jpg"/>
        <ma:duration rdf:datatype="http://www.w3.org/2001/XMLSchema#float">197</ma:duration>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/e289d823-3fc1-4e2d-9a1b-6330781e638c">
        <rdf:type rdf:resource="http://www.w3.org/ns/ma-ont#VideoTrack"/>
        <ma:title rdf:parseType="Literal">Tymur Melnyk - J.S. Bach Violin Concerto a-minor BWV 1041 - Vienna 1/3</ma:title>
        <ma:locator rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">https://www.youtube.com/watch?v=5uu5eOs_2ns</ma:locator>
        <ma:description rdf:parseType="Literal">www.tymur.com.</ma:description>
        <foaf:img rdf:resource="http://i.ytimg.com/vi/5uu5eOs_2ns/0.jpg"/>
        <ma:duration rdf:datatype="http://www.w3.org/2001/XMLSchema#float">246</ma:duration>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/f8037208-1a45-44fa-8631-72e96e580dd0">
        <rdf:type rdf:resource="http://www.w3.org/ns/ma-ont#VideoTrack"/>
        <ma:title rdf:parseType="Literal">Tymur Melnyk - J.S. Bach Violin Concerto a-minor BWV 1041 - Vienna 2/3</ma:title>
        <ma:locator rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">https://www.youtube.com/watch?v=9zNPRDYWKrQ</ma:locator>
        <ma:description rdf:parseType="Literal">www.tymur.com.</ma:description>
        <foaf:img rdf:resource="http://i.ytimg.com/vi/9zNPRDYWKrQ/0.jpg"/>
        <ma:duration rdf:datatype="http://www.w3.org/2001/XMLSchema#float">382</ma:duration>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/55471fa8-6646-4722-afa8-aa862cbd28a6">
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Vienna"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/94a8b6b7-1041-4ff9-96cb-f4b402c3a2a7">
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Vienna"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/1cd3adf2-4137-47b6-8b1d-4b7b809945f6">
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Vienna"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/e289d823-3fc1-4e2d-9a1b-6330781e638c">
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Vienna"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/f8037208-1a45-44fa-8631-72e96e580dd0">
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Vienna"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://images.ookaboo.com/photo/l/Josephinische_Landaufnahme_Vienna_2_l.jpg">
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Vienna"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://images.ookaboo.com/photo/l/ABK_2C_Vienna_June_2006_592_2_l.jpg">
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Vienna"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/55471fa8-6646-4722-afa8-aa862cbd28a6">
        <ma:hasKeyword rdf:resource="http://rdf.freebase.com/ns/en/vienna_philharmonic_orchestra"/>
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Vienna_Philharmonic"/>
        <ma:hasKeyword rdf:resource="http://musicbrainz.org/mm-2.1/artist/d770374d-05e9-4ed3-a068-3fbd4e6e4dd6/4"/>
        <ma:hasKeyword rdf:resource="http://rdf.freebase.com/ns/en/vienna"/>
        <ma:hasKeyword rdf:resource="http://rdf.freebase.com/ns/en/wieden"/>
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Wieden"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/94a8b6b7-1041-4ff9-96cb-f4b402c3a2a7">
        <ma:hasKeyword rdf:resource="http://rdf.freebase.com/ns/en/johann_sebastian_bach"/>
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Johann_Sebastian_Bach"/>
        <ma:hasKeyword rdf:resource="http://musicbrainz.org/mm-2.1/artist/24f1766e-9635-4d58-a4d4-9413f9f98a4c/4"/>
        <ma:hasKeyword rdf:resource="http://rdf.freebase.com/ns/en/scottish_chamber_orchestra"/>
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Scottish_Chamber_Orchestra"/>
        <ma:hasKeyword rdf:resource="http://musicbrainz.org/mm-2.1/artist/068632ae-2db3-4817-be30-f035fdc2478b/4"/>
        <ma:hasKeyword rdf:resource="http://rdf.freebase.com/ns/m/02x93k2"/>
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Ave_Maria_%28Bach/Gounod%29"/>
    </rdf:Description>

    <rdf:Description rdf:about="http://new.devserver.sti2.org:8080/lsi/resource/video/1cd3adf2-4137-47b6-8b1d-4b7b809945f6">
        <ma:hasKeyword rdf:resource="http://rdf.freebase.com/ns/en/jonathan_sass"/>
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Jonathan_Sass"/>
        <ma:hasKeyword rdf:resource="http://rdf.freebase.com/ns/en/johann_sebastian_bach"/>
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Johann_Sebastian_Bach"/>
        <ma:hasKeyword rdf:resource="http://musicbrainz.org/mm-2.1/artist/24f1766e-9635-4d58-a4d4-9413f9f98a4c/4"/>
        <ma:hasKeyword rdf:resource="http://rdf.freebase.com/ns/en/counterpoint"/>
        <ma:hasKeyword rdf:resource="http://dbpedia.org/resource/Counterpoint"/>
        <ma:hasKeyword rdf:resource="http://rdf.freebase.com/ns/en/vienna"/>
    </rdf:Description>

    </rdf:RDF>