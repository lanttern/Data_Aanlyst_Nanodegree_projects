#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a dictionary of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
"""
import codecs
import csv
import json
import pprint
import re

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}


def process_file(filename, fields):

    process_fields = fields.keys()
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            row = {}
            class_label = {}
            for key in process_fields:
                if len(line[key]) != 0:
                    line[key] = line[key].strip()
                    if line[key] == "NULL":
                        line[key] = None
                else:
                    continue
                
                if key == "rdf-schema#label":
                    if line[key] != None:
                        if "(" in line[key]:
                            row[fields[key]] = (line[key][:line[key].find("(")]).strip()
                        else:
                            row[fields[key]] = line[key]
                        print row[fields[key]]
                    else:
                        row[fields[key]] = None
                elif key == "name":
                    if line[key] == None or not is_name(line[key]):
                        row[fields[key]] = row["label"]
                    else:
                        row[fields[key]] = line[key]
                        
                elif key == "synonym":
                    if line[key] != None:
                        row[fields[key]] = parse_array(line[key])
                    else:
                        row[fields[key]] = line[key]
                elif key == "URI" or key == "rdf-schema#comment":
                    row[fields[key]] = line[key]
                else:
                    if line[key] != None and "|" in line[key]:
                        line[key] = parse_array(line[key])
                    class_label[fields[key]] = line[key]
                    row["classification"] = class_label
            data.append(row)        
            
    return data
def is_name(name):
    characters = [chr(c) for c in xrange(ord("a"), ord("z") + 1)]
    characters += [char.upper() for char in characters]
    if name == "NULL":
        return False
    else:
        for char in name:
            if char not in characters:
                return False
    return True

def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    data = process_file(DATAFILE, FIELDS)

    #pprint.pprint(data)
    assert data[0] == {
                        "synonym": None, 
                        "name": "Argiope", 
                        "classification": {
                            "kingdom": "Animal", 
                            "family": "Orb-weaver spider", 
                            "order": "Spider", 
                            "phylum": "Arthropod", 
                            "genus": None, 
                            "class": "Arachnid"
                        }, 
                        "uri": "http://dbpedia.org/resource/Argiope_(spider)", 
                        "label": "Argiope", 
                        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
                    }


if __name__ == "__main__":
    test()