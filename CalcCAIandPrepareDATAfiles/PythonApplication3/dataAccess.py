    
import pymssql

class dataAccess(object):
    """description of class"""
    def __init__(self,server,db,user,password):
            self.__server=server
            self.__db=db
            self.__user=user
            self.__password=password
            self.__conn = None
            self.__cursor = None

    def connect(self):
        self.__conn    = pymssql.connect(self.__server, self.__user, self.__password, self.__db)
        self.__cursor  = self.__conn.cursor()
        return True


    def execute(self,sql):
        self.__cursor.execute(sql)
        return self.__cursor
    
    def commit(self):
        self.__conn.commit()
        return True

    def disconnect(self):
        self.__conn.close()
        return True


