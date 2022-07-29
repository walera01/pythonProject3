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

    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT name, prise, description FROM posts WHERE id = {postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error output"+str(e))
        return (False, False)

    def getAllPost(self):
        try:
            self.__cur.execute(f"SELECT name, prise FROM posts ")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error output"+str(e))
        return (False, False)


    def addUser(self, name, password, email):
        try:
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)",(name, password, email))
            self.__db.commit()
            print("ok")
        except sqlite3.Error as e:
            print("Error add "+str(e))
            return False
        return True

    def chekEmail(self, email):
        try:
            self.__cur.execute(f"SELECT email FROM users WHERE email = (?) ", (email,))
            res = self.__cur.fetchone()
            if res:
                return False
        except sqlite3.Error as e:
            print("Error output"+str(e))
            return False
        return (True)

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = (?)", (email,))
            res = self.__cur.fetchone()
            if not res:
                print('user not found')
                return False
            return res
        except sqlite3.Error as e:
            print("Error output"+str(e))
        return False

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False
