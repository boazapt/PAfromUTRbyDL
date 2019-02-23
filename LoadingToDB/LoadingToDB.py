import pypyodbc 
import scipy.io
import io
import numpy as np

import h5py 

# finish run on 25/12/18
# only one bacteria we didn't found the ORF: deltadesulfotignum_balticum_dsm was not found

# connect to database according to 
# https://blogs.msdn.microsoft.com/cdndevs/2015/03/11/python-and-data-sql-server-as-a-data-source-for-python-applications/

cursorRead = cnxn.cursor()
cursorRead.execute('SELECT * FROM bacteria order by id')

connection = pypyodbc.connect("Driver={SQL Server};"
                        "Server=localhost;"
                        "Database=DNA;"
                        "uid=DNA;pwd=xxx")

runORFinsert=False
runUTRinsert=False

if runORFinsert:
    for row in cursorRead:
        #print('row = %r' % (row,))
        try:
            mat = scipy.io.loadmat('C:\\Users\\Administrator\\Documents\\research\\bacteria_ORF\\' + row['name'] + '_ORF.mat')
            listBarteriaORF=mat['final_ORF']
            #data = np.array(listBarteriaORF) # For converting to numpy array
            numOfORF=listBarteriaORF.shape[0];
            for i in range(numOfORF):
                cursorWrite = connection.cursor() 
                SQLCommand = ("INSERT INTO ORF (bacteriaID, geneID, ORF) VALUES (?,?,?)")
                currentORF=''.join(listBarteriaORF[i].item(0).tolist())
                Values = [row['id'],i,currentORF]
                cursorWrite.execute(SQLCommand,Values) 
                connection.commit() 
                i=i+1
        except:
            print('error on bacteria ' + row['name'] + ' maybe file was not found or something else')
            pass


if runUTRinsert:
    for row in cursorRead:
        print('row = %r' % (row,))
        try:
            mat = scipy.io.loadmat('C:\\Users\\Administrator\\Documents\\research\\bacteria_5utr\\' + row['name'] + '_UTR5.mat')
            listBarteriaUTR=mat['final_utr5']
            #data = np.array(listBarteriaORF) # For converting to numpy array
            numOfUTR=listBarteriaUTR.shape[0];
            for i in range(numOfUTR):
                cursorWrite = connection.cursor() 
                SQLCommand = ("INSERT INTO UTR5 (bacteriaID, geneID, UTR5) VALUES (?,?,?)")
                currentUTR=''.join(listBarteriaUTR[i].item(0).tolist())
                Values = [row['id'],i,currentUTR]
                cursorWrite.execute(SQLCommand,Values) 
                connection.commit() 
                i=i+1
        except:
            print('error on bacteria ' + row['name'] + ' maybe file was not found')
            pass

cnxn.close()








