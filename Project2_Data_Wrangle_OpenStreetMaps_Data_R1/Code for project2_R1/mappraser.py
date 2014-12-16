# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 21:24:59 2014

@author: zhihuixie
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output should be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
    """count tags"""
    tags ={}
    for event, elem in ET.iterparse(filename):
        if elem.tag not in tags:
            tags[elem.tag] = 1
        else:
            tags[elem.tag] = tags.get(elem.tag) + 1
    return tags


def output():
    """print output"""
    tags = count_tags('las-vegas_nevada.osm')
    pprint.pprint(tags)
def test():
    """For sample test"""
    tags = count_tags('sample.osm')
    pprint.pprint(tags)
    assert tags["node"] == 7350
    assert tags["bounds"] == 1
    assert tags["osm"] == 1
    assert tags["tag"] == 515 
    print "Pass"
    
if __name__ == "__main__":
    #test()
    output()