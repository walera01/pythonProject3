import pymysql
import yaml

from config import host,password,user,db_name


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
        with open('test.yaml', 'w') as f:
            yaml.dump(out, f, default_flow_style=False)
        # for i in out:
        #     print(i['id'],i['name'], '   =  ', i['cost'])
        #     print("-"*40)

        with open("test.yaml", 'r') as r:
            data= yaml.safe_load(r)
        print(data)
        # delete = "DROP TABLE `dildon`"
        # connect.execute(delete)
    finally:
        connection.close()
except Exception as ex:
    print("Dont connect")
    print(ex)