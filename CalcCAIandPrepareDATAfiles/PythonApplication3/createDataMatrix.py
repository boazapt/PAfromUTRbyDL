
from array import *
from random import randint
import numpy as np

import dataAccess as da

server      = "asdf"
db          = "DNA"
user        = "DNA"
password    = "asdf"
dataa    = da.pymssql.connect(server, user, password, "DNA")

# for NN the data will be like this: ACTATG we will get an array 1000 0010 0100 1000 0010 0001
# for Random Forest the data will be like this: ACTATG - we will get an array 1 2 4 1 4 3
# and we will add the CAI at the end

#load
#gg=np.load("train_data.npy")

if False:
    numberOfUTR5=50000
    LenOfUTR5sequence=50

    train_random_data = np.zeros( (numberOfUTR5, LenOfUTR5sequence*4+1) )
    for x in range(numberOfUTR5):
        for y in range(0,LenOfUTR5sequence*4,4):
            currentNucliutide=randint(0, 3)    # this will be replace with the nucliutide later
        
            if currentNucliutide==0:
                train_random_data[x,y:y+4]=[1,0,0,0]
            if currentNucliutide==1:
                train_random_data[x,y:y+4]=[0,1,0,0]
            if currentNucliutide==2:
                train_random_data[x,y:y+4]=[0,0,1,0]
            if currentNucliutide==3:
                train_random_data[x,y:y+4]=[0,0,0,1]
    
        currentLabel=randint(0, 9)        
        train_random_data[x,LenOfUTR5sequence*4] = currentLabel   

    # remark because i don't want to rewrite on the file:
    np.save("train_random_data_50000", train_random_data)

 
if False:
    numberOfUTR5=10000
    LenOfUTR5sequence=50

    train_random_data_for_random_forest = np.zeros( (numberOfUTR5, LenOfUTR5sequence+1) )

    for x in range(numberOfUTR5):
        for y in range(0,LenOfUTR5sequence):
            currentNucliutide=randint(1, 4)    # this will be replace with the nucliutide later
        
            train_random_data_for_random_forest[x,y]=currentNucliutide

       
        currentLabel=randint(0, 9)        
        train_random_data_for_random_forest[x,LenOfUTR5sequence] = currentLabel   

    # remark because i don't want to rewrite on the file:
    np.save("train_random_data_for_random_forest_50000", train_random_data_for_random_forest)

# ! ! ! remark - we can add column in CAI with random value 0/1/2 for each bacteria and then use it in the select for learning,training and testing.
# not so easy because we will also have to impliment the rate between them 
if True:
    #sql='select UTR5_5_to_3,CAI from UTR5 as a inner join geneExpressionEstimations as b on a.bacteriaID=b.bacteriaID and a.geneID=b.geneID'
    #sql='select UTR5_5_to_3, convert(numeric(4,3), CAI) as CAI from UTR5 as a inner join [temp_for_data14] as b on a.bacteriaID=b.bacteriaID and a.geneID=b.geneID'
    #sql='select UTR5_5_to_3, convert(numeric(4,3), CAI) as CAI from UTR5 as a inner join [temp_for_data14] as b on a.bacteriaID=b.bacteriaID and a.geneID=b.geneID where CAI>0.37 and cai<0.88'
    sql ='SELECT utr5_5_to_3, cai3 as CAI FROM [DNA].[dbo].temp_for_uniform1 where cai2>=0.38 and CAI2<0.88 and rownum<1501'
    
    # read from DB, we will have to add a filter and do blooks because we will have million records
    # loop on the records, for each prepare the 2 matrixes - one for NN and one for randm forest
    # save 2 files
    bacteria16s=[]
    cursor = dataa.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    numberOfUTR5=len(data)
    
    LenOfUTR5sequence=50 # we know that there are 50 letters in our UTR5 

    train_data_for_NN = np.zeros( (numberOfUTR5, LenOfUTR5sequence*4+1) )
    train_data_for_random_forest = np.zeros( (numberOfUTR5, LenOfUTR5sequence+1) )

    x=0                 # this is the number of UTR that we will move on (the lines)
    for item in data:
        UTR=item[0]
        CAI=item[1]     # the label values
        for y in range(LenOfUTR5sequence):
            currentNucliutide=UTR[y]    # this will be replace with the nucliutide later
        
            if currentNucliutide=='A':
                train_data_for_NN[x,y*4:y*4+4]=[1,0,0,0]
                train_data_for_random_forest[x,y]=1

            if currentNucliutide=='C':
                train_data_for_NN[x,y*4:y*4+4]=[0,1,0,0]
                train_data_for_random_forest[x,y]=2

            if currentNucliutide=='G':
                train_data_for_NN[x,y*4:y*4+4]=[0,0,1,0]
                train_data_for_random_forest[x,y]=3

            if currentNucliutide=='T':
                train_data_for_NN[x,y*4:y*4+4]=[0,0,0,1]
                train_data_for_random_forest[x,y]=4
   
        train_data_for_NN[x,LenOfUTR5sequence*4] = CAI 
        train_data_for_random_forest[x,LenOfUTR5sequence] = CAI
        
        x=x+1
    
    np.save("data_NN_1500_records_from038_to088_for_each_hundretch_of_each_bacteria_75000_Records", train_data_for_NN)
    np.save("data_random_forest_1500_records_from037_to087_for_each_hundretch_of_each_bacteria_75000_Records", train_data_for_random_forest)

    
l=3

