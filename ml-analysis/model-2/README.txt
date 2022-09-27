First we need to extract the features from the binary files, to perform analysis.

We used the set "64-Bit Windows PE files" (997 samples) from VirusShare for our model. The dataset has not been attached, but the extracted features are present in data.csv.

We have also provided 6 examples of binary files that were shown in the demo.

To extract the features from binary files, run:
python extract.py

To run the KNN model, run:
python run_KNN.py

