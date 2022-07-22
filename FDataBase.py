import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql="""SELECT * FROM mainmenu"""
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Error read from database")
        return []

    def addPost(self, name, prise, description):
        try:
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?)",(name, prise, description))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error add "+str(e))
            return False
        return True