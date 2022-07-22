from flask import Flask, render_template, request, flash, g
import sqlite3
import os

# конфигурация
from FDataBase import FDataBase

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Создание таблиц в БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    """СОЕДИНЕНИЕ С ДБ ЕСЛИ ЕГО ЕЩЁ НЕТ"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def closer_db(error):
    """ЗАКРЫВАЕМ СОЕДИНЕНИЕ С ДБ"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/add', methods=['POST', 'GET'])
def add_db():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['name']) > 4 and request.form['prise'] and len(request.form['description'])>10:
            print(request.form['name'], request.form['prise'], request.form['description'])
            res = dbase.addPost(request.form['name'], request.form['prise'], request.form['description'])
            if not res:
                flash('Error addPost', category='error')
            else:
                flash("Excelent",  category='success')
        else:
            flash('smoll description', category='error')

    return render_template('add.html', title="Добавление записи")

@app.route('/')
def main():
    return render_template('base.html', title="Главная")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        print(request.form)
        if len(request.form['name'])>2:
            flash('Отлично', category='success')
        else:
            flash('Что-то ввели неправильно', category='error')
    return render_template('login.html', title="Авторизация")

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Ошибка")



if __name__ == "__main__":
    app.run(debug=True)

    # try:
    # create_table = "CREATE TABLE `dildon`(id int AUTO_INCREMENT,"\
    #         "name varchar(35),"\
    #         "cost varchar (8),"\
    #         "PRIMARY KEY(id));"
    # connect.execute(create_table)
    # weight = '80sm'
    #
    # input_data = "INSERT INTO `dildon`(name, cost) VALUES (%s,'20$'),('25sm','25$');"
    # connect.execute(input_data, weight)
    # connection.commit()
    #
    # output_data = "SELECT * FROM `dildon` ORDER BY id DESC ;"
    # connect.execute(output_data)
    # out = connect.fetchall()
    # print("-"*40)
    #
    # for i in out:
    #     print(i['id'],i['name'], '   =  ', i['cost'])
    #     print("-"*40)
    #
    # # delete = "DROP TABLE `dildon`"
    # # connect.execute(delete)


