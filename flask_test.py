from flask import Flask, render_template, request, flash, g, abort, redirect, url_for
import sqlite3
import os
from UserLogin import UserLogin

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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


login_manager = LoginManager(app)
login_manager.login_view = 'login'    #перенаправление если неавторизованный переходит на запрещенную страницу
login_manager.login_message = "Autorization for access"  #сообщение при переходе на страницу для зарегестрированных
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return UserLogin().fromDB(user_id, dbase)

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

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.teardown_appcontext
def closer_db(error):
    """ЗАКРЫВАЕМ СОЕДИНЕНИЕ С ДБ"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/add', methods=['POST', 'GET'])
def add_db():
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
    allpost = dbase.getAllPost()
    return render_template('main.html',allpost=allpost, title="Главная")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False  # запоминание сохранения пользователя
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for('main')) #смотрит с какого урл перенаправило и после авторизации туда и отправляет
        flash("wrong password", category="error")
    return render_template('login.html', title="Авторизация")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['name'])>2:
            if request.form['password'] == request.form['password_again']:
                if dbase.chekEmail(request.form['email']):
                    res = dbase.addUser(request.form['name'], generate_password_hash(request.form['password']), request.form['email'])
                    if res:
                        flash('Вы зарегистрированы', category='success')
                    else:
                        flash("Что-то пошло не так", category="error")
                else:
                    flash('Такой email существует', category='error')
            else:
                flash('Пароли не совпадают', category='error')
        else:
            flash('Имя слишком короткое', category='error')
    return render_template('register.html', title="Авторизация")


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Ошибка")

@app.route('/post/<int:id_post>')
@login_required
def showPost(id_post):

    name, prise, description = dbase.getPost(id_post)
    if not name:
        abort(404)
    content={
        'name':name,
        'prise': prise,
        'description':description
    }
    return render_template('post.html', content=content )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout successfull", category="success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return f"""<a href="{url_for('logout')}">Выйти из профиля</a>
                user info: {current_user.get_id()}"""

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


