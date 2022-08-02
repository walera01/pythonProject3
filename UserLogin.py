from flask import url_for
from flask_login import UserMixin
from flask import Flask

app = Flask(__name__)



class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self,user):
        self.__user = user
        return self

    #
    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):                  #UserMixin это всё имеет
    #     return True
    #
    # def is_anonymous(self):
    #     return False
    def get_id(self):
        return str(self.__user['id'])

    def get_name(self):
        return str(self.__user['name'])

    def get_email(self):
        return str(self.__user['email'])

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Image not found" + str(e))
            else:
                img = self.__user['avatar']

        return img