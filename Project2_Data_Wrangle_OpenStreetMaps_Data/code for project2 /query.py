# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 20:58:02 2014
run mongodb.py code to create database before run this program
@author: zhihuixie
"""
from pymongo import MongoClient
import pprint
from mongodb import load_data

def get_db(database):
    """This function insert data to MongoDB"""
    client = MongoClient('localhost:27017') #get client
    db = client[database] #build database
    return db

def get_query(data, db): 
    """This function measure number of all types of amenities"""
    queries = []
    stats = {}
    for index in range(len(data)): #setup all types of amenities in data
        #print data[index][u'name:ka']
        if "amenity" in data[index]:
            item = data[index]["amenity"]
            if item not in queries:
                queries.append(item)
    for query in queries: #calculate number of each type of amenity
        stats[str(query)] = db.las_vegas_map_dataset.find({"amenity": query}).count()
    return stats

def get_pipeline():
    """This function build pipeline for queries"""
    #hotels as amenity
    pipeline1 = [{"$match": {"amenity": "hotel"}},
                 {"$project":{"_id": "$name", "cuisine": "$cuisine", "phone": "$phone"}}]
    #hotels as tourism
    pipeline2 = [{"$match": {"tourism": "hotel"}},
                 {"$project":{"_id": "$name", "address": "$address", "phone": "$phone"}}]      
    #mall as amenity
    pipeline3 = [{"$match": {"amenity": "mall"}},
                 {"$project":{"_id": "$name", "cuisine": "$cuisine", "phone": "$phone"}}]  
    #mall as shop
    pipeline4 = [{"$match": {"shop": "mall"}},
                 {"$project":{"_id": "$name", "address": "$address", "phone": "$phone"}}]    
    #top 5 contributors to the map    
    pipeline5 = [{"$match": {"created.user": {"$exists": 1}}},
                 {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 5}]
    return [pipeline1, pipeline2, pipeline3, pipeline4, pipeline5]

def output_result():
     """This function print output for queries"""
    
     db = get_db("las_vegas_map_dataset")
     """
     data = load_data("las-vegas_nevada.osm.json") 
     stats = get_query(data, db) #print number of each type of amenity
     print stats
     """
     pipelines = get_pipeline()
     describ = ["Hotels as amenity: ", "Hotels as tourism: ", "Malls as amenity: ", "Malls as shop: ", "Top 5 contributors to the map: "]
     for index in range(len(pipelines)):
         result = db.las_vegas_map_dataset.aggregate(pipelines[index])
         print describ[index], len(result[u'result'])  
         pprint.pprint(result)  #print result of each pipeline
         print "\n"
    
def test():
    """This test is used for sample dataset"""
    db = get_db("sample_dataset")
    data = load_data("sample.osm.json"  )
    stats = get_query(data, db)
    pipelines = get_pipeline()
    result = db.sample.aggregate(pipelines[1])
    assert stats == {}
    assert result == {u'ok': 1.0, u'result': []}
    print "Pass tests"

    
if __name__ == "__main__":
    #test()
    output_result()