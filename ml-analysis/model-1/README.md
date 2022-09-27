# Static Analysis using Ember Dataset

We have used the Ember dataset which consists of feature set of 1.1 million PE executable binary files. The  dataset is divided in  400K malicious, 400K benign and 300K unlabeled files. The dataset comprises of 2.3K features like SHA256 and MD5 hashes, entropy of binary, headers related data, etc. Due to computation limit we have to train our model on 0.2 million samples and test on another 0.2 million samples. We tried many ML classifiers to classify the data some of them being  AdaBoost-SAMME algorithm, Multi-layer Perceptron Classifier, etc. Best accuracy of 86.5% was achieved using Random Forest Classifier.

## How to run code
You can execute the code by simply running the jupyter notebook. But please note that it will download the ember dataset whose download size is around 1.5gb and storage size is around 10gb, so you must be prepared with that amount of storage. Also, training it will require a lot of RAM and might give error if less RAM is present or may slow down running of script by large amount.

The code downloads the ember git repository and installs it as a pip package (Change the first line of code according to your system for eg. using conda, etc). In the directory specified by variable `main_data_dir` all data gets downloaded and vectorized data is prepared for training models. Since, data is quite large we randomly select some rows from data for training. Then, using sklearn classifiers, we build models from training data and store best models according to score obtained by testing models on test data.

## Best Accuracy of best classifiers
1. Random Forest Classifier: 89.3%
2. Decision Tree Classifier: 84.2%
3. ADA Boost Classifier: 83.1%

Best accuracy of other classifiers was quite variable which varied in between 50% to 80%. Among them a few classifiers like Gaussian Process Classsifiers, K-Neighbours classifiers with large k, etc took a lot of time to run even for small dataset and hence could not be tested with large data.
