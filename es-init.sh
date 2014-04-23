curl -XDELETE 'http://localhost:9200/lsi/'

curl -XPUT 'http://localhost:9200/lsi/'

curl -XPUT 'http://localhost:9200/lsi/media/_mapping' -d '
{
    "media" : {
        "properties" : {
            "status" : {"type" : "string", "store" : "yes", "index" : "analyzed"},
            "locator" : {"type" : "string", "store" : "yes", "index" : "analyzed"},
            "title" : {"type" : "string"},
            "description" : {"type" : "string"},
            "source" : {"type" : "string", "store" : "yes", "index" : "analyzed"},
            "created" : {"type" : "date", "store" : "yes", "index" : "analyzed"},
            "_timestamp" : {"enabled" : true, "path" : "created", type: "date"},
            "query_lod" : {"type" : "string", "store" : "yes", "index" : "analyzed"},
            "query_context" : {"type" : "string", "store" : "yes", "index" : "analyzed"},
            "width" : {"type" : "long", "store" : "yes", "index" : "analyzed"},
            "height" : {"type" : "long", "store" : "yes", "index" : "analyzed"},
            "created" : {"type" : "date", "store" : "yes", "index" : "analyzed"},
            "published" : {"type" : "date", "store" : "yes", "index" : "analyzed"},
            "latitude" : {"type" : "double", "store" : "yes", "index" : "analyzed"},
            "longitude" : {"type" : "double", "store" : "yes", "index" : "analyzed"},
            "location_name" : {"type" : "string", "store" : "yes", "index" : "analyzed"},
            "author_name" : {"type" : "string", "store" : "yes", "index" : "analyzed"},
            "author_uri" : {"type" : "string", "store" : "yes", "index" : "analyzed"},
            "keywords" : {"type" : "string", "store" : "yes", "index" : "analyzed"}
        }
    }
}'

curl -XPUT 'http://localhost:9200/lsi/video/_mapping' -d '
{
    "video" : {
        "_parent" : {"type" : "media"},
        "properties" : {
            "duration" : {"type" : "long"},
            "thumbnail" : {"type" : "string"}
        }
    }
}'

curl -XPUT 'http://localhost:9200/lsi/image/_mapping' -d '
{
    "image" : {
        "_parent" : {"type" : "media"}
    }
}'
