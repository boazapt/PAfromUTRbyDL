
import numpy as np

import bacteria as a

import dataAccess as da


server      = "212.235.125.48"
db          = "DNA"
user        = "DNA"
password    = "0.5 way done"

#dataa=da.dataAccess(server,db,user,password)
dataa    = da.pymssql.connect(server, user, password, "DNA")

# load from file (should be insert to bacteria class)
#with open('bacteriaObject1.pkl', 'rb') as input:
#        a=pickle.load(input)

a=a.bacteria()

#a.set_suggested_aSD(['GGCTGG'])         # the value might be taken from DB instead of setting it here

for i in range(621,1110):
    a.laodFrom_DB_ByBacteriaID(dataa,i)
    a.calc_CAI(dataa)

#a.calc_CAI(dataa)