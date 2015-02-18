# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 20:35:11 2015

@author: zhihuixie
"""
import pickle
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import RandomizedPCA
from sklearn.metrics import accuracy_score, precision_score, recall_score

def explore_data(enron_data):
    """ This functon explore characteristics of enron data """
    total_data_point = 0
    valid_data_point = 0
    number_of_poi = 0
    features = []
    invalid_data_by_person = {}
    for name, value in enron_data.items():
        total_data_point += len(value)     ### calculate total data point
        invalid_data_point = 0
        for feature in value:
            if feature not in features and feature != "poi" \
                and feature != "email_address":
                features.append(feature)    ### features in enron dataset
            if value[feature] != "NaN":
                valid_data_point += 1    ### calculate valid data point
            if value[feature] == "NaN":
                invalid_data_point += 1 
            if feature == "poi":
                if value[feature] == True:
                    number_of_poi += 1    ### calculate number of poi
        invalid_data_by_person[name] = invalid_data_point
    return (total_data_point, valid_data_point, number_of_poi, len(features),\
        features, invalid_data_by_person)

def identify_outliers(invalid_data_by_person, number_of_features):
    """ this function identify outliers including invalid names and invalid data"""
    ### identify invalid names: usually names include first, last and/or middle name
    ### so the length of words in name should be 2 or 3, names with unusual 
    ### length maybe invalid
    outliers = [person for person in invalid_data_by_person \
         if len(person.split()) < 2 or len(person.split()) > 4]
    ### exclude person with more than 95% invalid data points    
    outliers += [name for name in invalid_data_by_person \
        if invalid_data_by_person[name] > 0.95*number_of_features]
    return outliers

def remove_outliers(enron_data, outliers):
    """ this function remove outliers"""
    for name in outliers:
        enron_data.pop(name, 0)
        
def creat_new_features(enron_data):
    """ this function adds new features to enron data and return new features """
    new_features = ["total_asset", "fraction_of_messages_with_poi"]  # add two features
    asset = ["salary", "bonus", "total_stock_value", "exercised_stock_options"]
    messages = ["to_messages", "from_messages", "from_poi_to_this_person", \
        "from_this_person_to_poi"]
    for name, value in enron_data.items():
        valid_asset_value = True
        valid_message_value = True
        for key in asset:
            if value[key] == "NaN":
                valid_asset_value = False
                break
        for key in messages:
            if value[key] == "NaN":
                valid_message_value = False
                break
        if valid_asset_value:
            ### sum total asset if data are valid
            value[new_features[0]] = sum([value[key] for key in asset]) 
        else:
            ### assign value to NaN if having invalid data
            value[new_features[0]]  = "NaN"
        if valid_message_value:
            ### calculate fraction of message interacting with poi
            all_messages = value["to_messages"] + value["from_messages"]
            messages_with_poi = value["from_poi_to_this_person"] + \
                value["from_this_person_to_poi"]
            value[new_features[1]] = float(messages_with_poi)\
                /all_messages
        else:
            ### assign value to NaN if having invalid data
            value[new_features[1]] = "NaN"
    return new_features

def clf_evaluation(clf, features, labels, trials, is_pca, n):
    """ an evaluation function for machine learning algorithm: accuracy_score,
        precision and recall
    """
    score = []
    precision = []
    recall = []
    # run 2000 trials and get mean values
    for trial in range(trials): 
        features_train, features_test, labels_train, labels_test = \
            train_test_split(features, labels, test_size = 0.3, random_state = 42)
        if is_pca:
            pca = RandomizedPCA(n_components = n, whiten=True).fit(features_train)
            features_train = pca.transform(features_train)
            features_test = pca.transform(features_test)
        clf.fit(features_train, labels_train)
        pred = clf.predict(features_test)
        score.append(accuracy_score(pred, labels_test))
        precision.append(precision_score(pred, labels_test))
        recall.append(recall_score(pred, labels_test))
    return (np.mean(score), np.mean(precision), np.mean(recall))

if __name__ == "__main__":
    enron_data = pickle.load(open("final_project_dataset.pkl", "r"))
    (total_data_point, valid_data_point, number_of_poi, number_of_features, \
        features, invalid_data_by_person) = explore_data(enron_data)
    print "Total data point in enron dataset:", total_data_point, "\n"
    print "Valid data point in enron dataset:", valid_data_point, "\n"
    print "Number of poi in enron dataset:", number_of_poi, "\n"
    print "Number of features in enron dataset:", number_of_features, "\n"
    print "Features in enron dataset:\n", features
    outliers = identify_outliers(invalid_data_by_person, number_of_features)
    print "Outliers in enron dataset:\n", outliers
    remove_outliers(enron_data, outliers)
    creat_new_features(enron_data)
    #print enron_data 
