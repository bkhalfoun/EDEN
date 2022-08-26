# EDEN
Welcome to EDEN, a Location Privacy Protection Mechanism based on a federated risk assessment FURIA.

You can :

- Apply a set of LPPMs with different configuations, namely: Promesse, Geo-indistinguishability thanks to Accio project and Trilateration.
- Apply a set of re-identification attacks, namely: POI-Attack, PIT-Attack and AP-Attack thanks using accio project. 
- Train and test FURIA, a federated user re-identification attack model. We provide an exemple on Privamov mobility dataset where multiple rounds are considered. We suppose a training round is done every night, after collecting the mobility data of the user during the day. 
- Apply EDEN: Considering three LPPMs: Geoi, Promesse and Trilateration with three configuration each (please refer to the paper).

# Format of Mobility Datasets 

multiple subtraces of mobility per user = multiple CSV files named <user_id_seq>.csv

CSV file format = Each line is a record of the mobility trace.

One record = <lattitude,longitude,timestamp>

Timestamp = Unix time POSIX.

# Apply LPPM and convert data to feature vectors

bash run_LPPMs-train-SERVER.sh [data] [level=15] [nameOutput] "1" [pathToSourceFiles]  [workingDirectory] [promesse-distance=200.meters] [geoi-epsilon=0.01] [trl-range=2]
 
NB: Install S2Geometry library for python as illustated in https://s2geometry.io/about/platforms

# Run Re-identification Attacks 

bash run_single_attacks.sh [pathToTrainData]  [pathToTestData] [xdays=15days] [datasetName] [lppmName]  [workdir] [pathToSourceFiles]
  
# Run FURIA, the federated user re-identification attack

We provide an example of Privamov Dataset. Thus, here is the link for preprocessed data (feature vectors of non-obfuscated and obfuscated data previously generated): https://drive.google.com/drive/folders/1FGxqMLihNVD8rq7LCqg1UrnraUN_1cXS?usp=sharing

The notebook includes : 

1- Setting ( prepare inputs and model parameters)

2- Data preprocessing (Uniforming features, verifying timestamps, Reducing and centering, Normalizing IDs)

3- Generate DRk (Data Round "k") : prepare mobility data of each round (i.e., each day) per user.

4- Generate models (AFi).

5- Test Model AFi with DRi+1.

# Run EDEN 

Once the experiment of FURIA is done (i.e., the federated model of each round is generated), collect the testing result of predictions of each round in "<ProjectName>/Evaluation/<datasetName>/Predictions/" 

Concatenate the utility metric values to each Prediction with prepareUtility-perDay.py

Then, run: python  EDEN.py [pathToPredictions] [outputDirectory] [outputFile]
  
[outputDirectory] : contains, for each round, protected users against AF model of FURIA. 

[outputFile] : has the following columns 'Dataset','Lppm','Model','Round', 'Nb_user','Correct', 'Total','Accuracy'.

# Paper 

Khalfoun, B., Ben Mokhtar, S., Bouchenak, S., & Nitu, V. (2021). EDEN: Enforcing Location Privacy through Re-identification Risk Assessment: A Federated Learning Approach. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, 5(2), 1-25.


# Contact

besma.khalfoun@insa-lyon.fr
