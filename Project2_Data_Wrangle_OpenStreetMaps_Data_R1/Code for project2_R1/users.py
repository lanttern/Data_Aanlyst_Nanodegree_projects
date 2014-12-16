#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    """add unique user to set"""
    user = set()
    if "uid" in element.attrib:
        user.add(element.attrib["uid"])
    return user

def process_map(filename):
    """process file iternatively"""
    users = set()
    for _, element in ET.iterparse(filename):
        users.update(get_user(element))
    return users


def output():
    """print unique users"""
    users = process_map('las-vegas_nevada.osm')
    pprint.pprint(users)
    print len(users)

def test():
    """for sample test"""
    users = process_map('sample.osm')
    pprint.pprint(users)
    assert len(users) == 93
    print "Pass"

if __name__ == "__main__":
    #test()
    output()