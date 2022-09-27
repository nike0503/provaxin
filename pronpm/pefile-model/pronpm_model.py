'''
As this is a KNN model, there is no such thing as a "trained model",
since KNN runs by evaluating the test data point's distance from
all the training data points at runtime.

Hence, data.csv has to be included while running the model.
data.csv was obtained by running the extractor file on the dataset.
'''

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

if len(sys.argv) < 2:
    print("Syntax: python pronpm_model.py <featuresFile.csv>")

evaluationFile = sys.argv[1]

# Importing the dataset
dataset = pd.read_csv('data.csv', sep = '|')
X = dataset.drop(['Name', 'md5', 'legitimate'], axis = 1).values
y = dataset['legitimate'].values

# For evaluation:
evaluation_dataset = pd.read_csv(evaluationFile, sep = '|')
X_evaluation = evaluation_dataset.drop(['Name', 'md5', 'legitimate'], axis = 1).values
y_evaluation = evaluation_dataset['legitimate'].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X_evaluation = sc.transform(X_evaluation)


# Fitting K-NN to the Training set
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 4, metric = 'minkowski', p = 2)
classifier.fit(X_train, y_train)

# Predicting whether the evaluation file is safe
# 1 -> safe, 0 -> malicious
print(classifier.predict(X_evaluation))
