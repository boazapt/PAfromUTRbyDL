# Predicting PA from UTR genome data using deep learning

## Introduction

This project is a deep leanrning prediction model for Protein Abundance levels based on the 50nt upstream of the start codon (UTR5)

## Directories:
1. models - contain the file PAfromUTRbyDL.ipynb, jupyter notebook for training and evaluating the our models
2. CalcCAIandPrepareDATAfiles - contain the scripts for calculating the CAI and prepare the data files
  - calcCAI.py - script for calculating the CAI values for each bacteria
  - createDataMatrix.py - script for building data file for the networks
  - bacteria.py - class for bacteria with help functions
  - dataAccess.py - calss for connection DB
  - data_NN_1500_records_from038_to088_for_each_hundretch_of_each_bacteria_75000_Records.zip - file with 75K labeled data for
    the fully connected and CNN models
  - data_random_forest_1500_records_from037_to087_for_each_hundretch_of_each_bacteria_75000_Records.zip - file with 75K labeled
    data for the random forest model
3. LoadingToDB - contain script for extracting raw data and upload to DB

If you have any question or want to run with more data, please email us. We have processed 2.2M labeled records. 

## Contacts:

boazapt@mail.tau.ac.il or doryaniv@mail.tau.ac.il
