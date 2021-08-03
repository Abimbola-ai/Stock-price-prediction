import psycopg2
from decouple import config

class DatabaseError(psycopg2.Error):
    pass

class Database:

    def __init__(self) -> None:
        self.__connection = None
        self.__cursor = None

    def connect(self):
        url = config("DATABASE_URL")
        try:
            self.__connection = psycopg2.connect(url)
                                # dbname = config("db_name"),
                                # port = config("db_port"),
                                # host = config("db_host"),
                                # user = config("db_user"),
                                # password = config("db_password"))
        
            self.__connection.autocommit = True
            self.__cursor = self.__connection.cursor()
            return self.__cursor
        except (Exception, DatabaseError):
            raise DatabaseError("Unable to connect to the database")
    
    def create_tables(self):
        try:
            self.__cursor.execute("CREATE TABLE IF NOT EXISTS Data\
                        (id SERIAL PRIMARY KEY, \
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\
                             ticker_name VARCHAR(10), years_analysed INT, Future_price FLOAT)")
            print("Database table created")
       
        except (Exception, DatabaseError):
            raise DatabaseError("Unable to create table")

    def delete_tables(self):
        try:
            self.__cursor.execute("DROP TABLE IF EXISTS Data CASCADE")
            print("Table successfully dropped")
        
        except (Exception, DatabaseError):
            raise DatabaseError("Unable to drop table")
if __name__=="__main__":
    d = Database()
    d.connect()
    d.create_tables()
  