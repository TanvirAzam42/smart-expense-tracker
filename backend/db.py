from flask_mysqldb import MySQL

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'tanvir@1234'
    app.config['MYSQL_DB'] = 'expense_tracker'

    mysql.init_app(app)