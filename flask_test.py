from flask import Flask, render_template, request, flash
import pymysql
from connector import host,password,user,db_name


try:
    connection = pymysql.connect(
        host = host,
        password = password,
        port=3306,
        user=user,
        database=db_name,
        cursorclass = pymysql.cursors.DictCursor,
    )
    print("successfully ")
    try:
        connect  = connection.cursor()
        # create_table = "CREATE TABLE `dildon`(id int AUTO_INCREMENT,"\
        #         "name varchar(35),"\
        #         "cost varchar (8),"\
        #         "PRIMARY KEY(id));"
        # connect.execute(create_table)
        weight = '80sm'

        input_data = "INSERT INTO `dildon`(name, cost) VALUES (%s,'20$'),('25sm','25$');"
        connect.execute(input_data, weight)
        connection.commit()

        output_data = "SELECT * FROM `dildon` ORDER BY id DESC ;"
        connect.execute(output_data)
        out = connect.fetchall()
        print("-"*40)

        for i in out:
            print(i['id'],i['name'], '   =  ', i['cost'])
            print("-"*40)

        # delete = "DROP TABLE `dildon`"
        # connect.execute(delete)
    finally:
        connection.close()
except Exception as ex:
    print("Dont connect")
    print(ex)

app = Flask(__name__)
app.config['SECRET_KEY']='sdfasdfasd'

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