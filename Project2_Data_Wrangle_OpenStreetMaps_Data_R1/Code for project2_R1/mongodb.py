# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 20:58:02 2014

@author: zhihuixie
run data.py code to generate"~osm.json" file before run this program
"""
from pymongo import MongoClient
import json
import codecs

def get_db(database, data):
    """This function insert data to MongoDB"""
    client = MongoClient('localhost:27017') #get client
    db = client[database] #build database
    for item in data:  
        db.las_vegas_map_dataset_R1.insert(item)  #insert data
    return db

def load_data(filename):
     """This function print output for queries"""
     data = []
     with open(filename) as f:
        for line in f:
            while True:
                try:
                    jfile = json.loads(line.encode("utf-8"))
                    break
                except ValueError:
                # Not yet a complete JSON value
                    line += next(f)
            data.append(jfile)
     print "Load data successfully"
     return data
     
def insert_data():
    data = load_data("las-vegas_nevada.osm.json")
    get_db("las_vegas_map_dataset_R1", data)
    print "Insert data to database completed"
    
def test():
    data = load_data("sample.json")
    get_db("sample_dataset", data)
    print "Insert data to database completed"
    
if __name__ =="__main__":
    insert_data()
    #test()
         