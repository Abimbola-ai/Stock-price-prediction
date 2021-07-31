from database import db

class DataError(Exception):
    pass

class Data:
    def __init__(self, cursor = db().connect()) -> None:
        self.__cursor = cursor
    
    def select_all(self):
        self.__cursor.execute("SELECT * FROM Data")
        return self.__cursor.fetchall()
    
    def add_data(self):
        try:
            self.__cursor.execute("INSERT INTO Data (ticker, years, Future_price)\
            VALUES (:ticker, :years, :prediction)") #,{"ticker": ticker, "years": years, "Future_price":prediction})
            print("Record added successfully")
        except DataError:
            raise DataError("Unable to add record")

