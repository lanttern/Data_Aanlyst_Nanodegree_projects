#!/usr/bin/python

#import matplotlib.pyplot as plt
import sys
import pickle
sys.path.append("../tools/")
from enron_data_help_function import *
from copy import copy
from feature_format import featureFormat
from feature_format import targetFeatureSplit

### "poi" is a target label
target_label = ["poi"]

## 1. Data pre-processing 
### 1.1 load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )

### 1.2 explore data
(total_data_point, valid_data_point, number_of_poi, number_of_features, \
    features_list, invalid_data_by_person) = explore_data(data_dict)
print "Total data point in enron dataset:", total_data_point, "\n"
print "Valid data point in enron dataset:", valid_data_point, "\n"
print "Number of poi in enron dataset:", number_of_poi, "\n"
print "Number of features in enron dataset:", number_of_features, "\n"

### 1.3 identify outliers
outliers = identify_outliers(invalid_data_by_person, number_of_features)
print "Outliers in enron dataset:\n", outliers, "\n"

### 1.4 remove outliers
remove_outliers(data_dict, outliers)

### 1.5 add new features
new_data_dict = copy(data_dict)
is_add_features = True
print "Set add_features as:", is_add_features, "\n"
if not is_add_features:
    features_list = target_label + features_list
if is_add_features:
    features_list = target_label + features_list + creat_new_features(new_data_dict)
    data_dict = new_data_dict

### 1.6 format data and split labels and features
data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

### 1.7 rescale features
from sklearn import preprocessing
scaler = preprocessing.MinMaxScaler()
features = scaler.fit_transform(features)

## 1.8 feature selection: k-best
from sklearn.feature_selection import SelectKBest
if is_add_features:
    k_features = 10
else:
    k_features = 10
k_best = SelectKBest(k=k_features)
k_best.fit(features, labels)
scores = k_best.scores_
feature_and_score = sorted(zip(features_list[1:], scores), key = lambda l: l[1],\
     reverse = True)

features_list = target_label + [feature for (feature, score) in \
    feature_and_score][:k_features]
print "Top 10 features and scores:\n", feature_and_score[:k_features], "\n"
print "My features:\n", features_list, "\n"

### 1.9 redo format data and split labels and features
data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)
features = scaler.fit_transform(features)

## 2. try PCA or not
is_pca = True
n = 5
print "Set pca as:", is_pca, "\n"
trials = 500
### 2.1 try algorithms: supervised learning: Support Vector Machines,
### Stochastic Gradient Descent, Gaussian Naive Bayes, Random Forests 
### unsupervised learning: K-means
### Support Vector Machines
from sklearn import svm
s_clf = svm.SVC(kernel="rbf")

### Stochastic Gradient Descent
from sklearn import linear_model
g_clf = linear_model.SGDClassifier(class_weight = "auto")

### Gaussian Naive Bayes
from sklearn.naive_bayes import GaussianNB
nb_clf = GaussianNB()

### Random Forests
from sklearn.ensemble import RandomForestClassifier
r_clf = RandomForestClassifier()

### K-means
from sklearn import cluster
k_clf = cluster.KMeans(n_clusters=2)

### 2.2 evulations:
print "(score, precision, recall) using Support Vector Machines:",\
    clf_evaluation(s_clf, features, labels, trials, is_pca, n), "\n"
print "(score, precision, recall) using Stochastic Gradient Descent:",\
    clf_evaluation(g_clf, features, labels, trials, is_pca, n), "\n"
print "(score, precision, recall) using GaussianNB:",\
    clf_evaluation(nb_clf, features, labels, trials, is_pca, n), "\n"
print "(score, precision, recall) using Random Forests:",\
    clf_evaluation(r_clf, features, labels, trials, is_pca, n), "\n"
print "(score, precision, recall) using K-means:",\
    clf_evaluation(k_clf, features, labels, trials, is_pca, n), "\n"

## 3. optimization: tune parameters for Stochastic Gradient Descent
from sklearn import grid_search
trials = 1
parameters = {"loss":("hinge", "log", "modified_huber", "perceptron", \
    "epsilon_insensitive",  "huber"), "n_iter":[1,5,10,20, 50, 100, 200, 500],\
    "alpha": [1e-15, 1e-10, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]}
g_clf = grid_search.GridSearchCV(g_clf, parameters)
print "(score, precision, recall) using optimized Stochastic Gradient Descent:",\
    clf_evaluation(g_clf, features, labels, trials, is_pca, n), "\n"
g_clf =  g_clf.best_estimator_

## 4. final selection and evulation
clf = nb_clf

## 5. dump settings
### dump your classifier, dataset and features_list so 
### anyone can run/check your results
pickle.dump(clf, open("my_classifier.pkl", "w") )
pickle.dump(data_dict, open("my_dataset.pkl", "w") )
pickle.dump(features_list, open("my_feature_list.pkl", "w") )


