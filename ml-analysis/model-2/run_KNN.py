#!/usr/bin/env python3

# K-Nearest Neighbors (K-NN)

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('data.csv', sep = '|')
X = dataset.drop(['Name', 'md5', 'legitimate'], axis = 1).values
y = dataset['legitimate'].values

# For Demo:
dataset_demo = pd.read_csv('data_demo.csv', sep = '|')
X_demo = dataset_demo.drop(['Name', 'md5', 'legitimate'], axis = 1).values
y_demo = dataset_demo['legitimate'].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X_demo = sc.transform(X_demo)


# Fitting K-NN to the Training set
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 4, metric = 'minkowski', p = 2)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)
print(accuracy_score(y_test, y_pred))

# Saving the Model:
import pickle
filename = "Model_2_KNN.sav"
pickle.dump(classifier, open(filename, 'wb'))
# Printing Demo Results:
print("--------DEMO RESULTS---------\n", classifier.predict(X_demo))

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

from sklearn.model_selection import cross_val_score
# creating odd list of K for KNN
myList = list(range(1,50))

# subsetting just the odd ones
neighbors = filter(lambda x: x % 2 != 0, myList)
neighbors = list(range(1,50))
# empty list that will hold cv scores
cv_scores = []

# perform 20-fold cross validation
for k in neighbors:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=20, scoring='accuracy')
    cv_scores.append(scores.mean())

# changing to misclassification error
# MSE = [1 - x for x in cv_scores]
# MSE_list = np.array(MSE)
# neighbors_list = np.array(neighbors)
# # determining best k
# optimal_k = neighbors[MSE_list.tolist().index(min(MSE_list))]
# print ("The optimal number of neighbors is %d" % optimal_k)


# plot misclassification error vs k
# plt.plot(neighbors_list, MSE_list)
# plt.xlabel('Number of Neighbors K')
# plt.ylabel('Misclassification Error')
# plt.show()
