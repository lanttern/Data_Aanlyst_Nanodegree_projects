#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_ref": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
MAPPING = {"St": "Street", "St.": "Street", "street": "Street", "AVE": "Avenue",
            "Ave": "Avenue", "Ave.": "Avenue", "Avene": "Avenue", "Avene.": "Avenue",
            "Rd": "Road", "Rd.": "Road", "Pkwy": "Parkway", 'Pkwy.': "Parkway",
            "Ln": "Lane", "Ln.": "Lane", "lane": "Lane",
            "Hwy": "Highway", "Hwy.": "Highway", "HWY": "Highway",
            "Expwy": "Expressway", "Expwy.": "Expressway",
            "Dr": "Drive", "Dr.": "Drive", "Blvd": "Boulevard", "Blvd.": "Boulevard", "N.": "North"}
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    """This function clean data and transform shape of element of data"""
    node = {}
    created = {}
    address = {}
    node_ref = []
    pos = [0, 0]
    if element.tag == "node" or element.tag == "way" :  #process 2 types of top level tags: "node" and "way"
        if element.tag == "node":
            node["type"] = "node"
        elif element.tag == "way":
            node["type"] = "way"
        for key in element.attrib:
            if key in CREATED:   #created attribute
                created[key] = element.attrib[key]
            elif key == "lat":
                pos[0] = float(element.attrib["lat"])
            elif key == "lon":
                pos[1] = float(element.attrib["lon"])
            else:
                node[key] = element.attrib[key]
        node["created"] = created   #created attribute
        node["pos"] = pos          #position attribute
        for tag in element.iter("tag"):
            k_value = tag.attrib["k"].strip()
            v_value = tag.attrib["v"].strip()
            if problemchars.search(k_value): #second level tag "k" value contains problematic characters, it's ignored
                continue
            elif "addr:" in k_value:   #second level tag "k" value starts with "addr:", added to a dictionary "address"
                if ":" not in k_value[5:]:    #there is a second ":" that separates the type/direction of a street,the tag is ignored
                    name = v_value
                    name = name.replace(",", "")
                    for word in name.split(" "):  #treat address type
                        if word in MAPPING.keys():
                            name = name.replace(word, MAPPING[word])
                    address[k_value[5:].strip()] = name
            elif k_value == "shop" and v_value == "mall":
                node["amenity"] = v_value
            elif k_value == "tourism" and v_value == "hotel":
                node["amenity"] = v_value    
            else:
                 node[k_value] = tag.attrib["v"].strip()
        if address != {}:
            node["address"] = address
        for nd in element.iter("nd"):  #add node_ref
            node_ref.append(nd.attrib["ref"])
        if node_ref != []:
            node["node_refs"] = node_ref
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    """this function create data"""
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('sample.osm', True)
    pprint.pprint(data)
    assert len(data) == 7350
    assert data[-1]["created"] == {'changeset': '5916730',
              'timestamp': '2010-09-30T02:38:10Z',
              'uid': '194231',
              'user': 'Chris Bell in California',
              'version': '3'}
    print "Pass"

def output():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    process_map('las-vegas_nevada.osm')
    print "process complete"

if __name__ == "__main__":
    output()
    #test()
