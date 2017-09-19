import sqlite3
import os

class Connection():
    def __init__(self, f):
        self.file_location = f;
        self.__connection = None

    def getConnection(self):
        if self.__connection is None:
            self.reconnect()

        return self.__connection;

    def reconnect(self):
        self.__connection = sqlite3.connect(self.file_location)
        self.__connection.row_factory = self.__rf

    def close(self):
        self.getConnection().close();
        self.__connection = None

    def exists(self):
        return os.path.isfile(self.file_location)

    #row factory
    def __rf(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d;
