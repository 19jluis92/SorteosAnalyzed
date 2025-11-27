import mysql.connector
import logging

class Database:


    def create_connection(self  ):
        context = mysql.connector.connect(
            host="localhost",
            user=self.user,
            password=self.password,
            db=self.dbName
        );
        return context;

    def __init__(self, dbName = "sorteos" , user = "root", password = "root"):
        self.logger = logging.getLogger('sorteosLogger');
        self.logger.info("STARTING DATABASE");
        self.dbName=dbName;
        self.user=user;
        self.password=password;
        self.dbconn = None;

    def queryMany(self,query):
        context = self.__enter__();
        cur = context.cursor();
        cur.execute(query);
        return cur.fetchall();

    def testDb(self):
        context = self.__enter__();
        cur = context.cursor();
        cur.execute("SELECT * FROM sorteos.numeros where sorteoId = 3 limit 3" );
        return cur.fetchall();

    def __enter__(self):
        self.dbconn = self.create_connection()
        return self.dbconn

    def __exit__(self):
        self.dbconn.close()
