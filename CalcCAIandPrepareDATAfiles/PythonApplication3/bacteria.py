import numpy as np
from CAI import CAI, relative_adaptiveness
import json

class bacteria:
    def __init__(self,bacteriaID=None,bacterianame=None,bacteriaORFs=None,bacteriaUTRs=None):
        self.__bacteriaID=bacteriaID        # bacteria property
        self.__bacterianame=bacterianame    # bacteria property
        self.__bacteriaORF=bacteriaORFs     # bacteria property
        self.__bacteriaUTRs=bacteriaUTRs    # bacteria property
        self.__geneCount=0                  # help parameter

    class ORF:
        def __init__(self,geneID,geneName,ORF):
            self.__geneID=geneID
            self.__geneName=geneName
            self.__ORF=ORF  
        def get_ORF(self):
            return self.__ORF

    class UTR5:
        def __init__(self,geneID,geneName,UTR5):
            self.__geneID=geneID
            self.__geneName=geneName
            self.__UTR5=UTR5
        def get_UTR5(self):
            return self.__UTR5
        def get_geneID(self):
            return self.__geneID

    def get_UTR5(self):
        return self.__bacteriaUTRs

    def get_ORF(self):
        return self.__bacteriaORF

    
    #############################################################################################
    # The function should get a bacteria ID that exist in DB and connection string
    # Then loads the neccesery things for the optimization algoritem 
    def laodFrom_DB_ByBacteriaID(self,dataa,bacteriaID):

        self.__bacteriaID=bacteriaID

        # for the bacteria Name:
        cursor = dataa.cursor()
        sql='SELECT [id] ,[Name] FROM bacteria where id=' + str(bacteriaID)
        cursor.execute(sql)
        row = cursor.fetchone()
        self.__bacterianame=row[1]

        #for the bacteria orf:
        cursorRead1 = dataa.cursor()
        cursorRead1.execute('SELECT [bacteriaID],[geneID],[geneName],[ORF_5_to_3],[insertDate] FROM [ORF] where bacteriaID='+str(bacteriaID))
        bacteriaORF=[]
        for row in cursorRead1:
            bacteriaORF.append(bacteria.ORF(row[1],row[2],row[3]))
        self.__bacteriaORF=bacteriaORF

        #for the bacteria utr5:
        cursorRead2 = dataa.cursor()
        cursorRead2.execute('SELECT [bacteriaID],[geneID],[geneName],[UTR5_5_to_3],[insertDate] FROM [UTR5] where bacteriaID='+str(bacteriaID))
        bacteriaUTR5=[]
        for row in cursorRead2:
            bacteriaUTR5.append(bacteria.UTR5(row[1],row[2],row[3]))
        self.__bacteriaUTRs=bacteriaUTR5


        return self


    #############################################################################################
    # calc weights according of all ORFs
    # Then loop on all the gene, calc the CAI for each and save to db
    # the python package that we use is CAI (https://pypi.org/project/CAI/)
    def calc_CAI(self,dataa):
        
        self.__geneCount=len(self.__bacteriaORF)

        concatORF=[]
         
        for i in range(self.__geneCount):
            currentORF=self.get_ORF()[i].get_ORF()
            concatORF.append(currentORF)
            
        weights = relative_adaptiveness(concatORF)   
            
        cursor = dataa.cursor()

        for i in range(self.__geneCount):
            currentCAIvalue=CAI(str(self.get_ORF()[i].get_ORF()), weights=weights)

            sql='INSERT INTO geneExpressionEstimations(bacteriaID, geneID, CAI) VALUES (' + str(self.__bacteriaID) + ' ,' + str(self.get_UTR5()[i].get_geneID()) + ' ,' + str(currentCAIvalue) + ')'
            
            cursor.execute(sql) 
           
            dataa.commit()

        
