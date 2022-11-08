from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'bf01b800f42366'
app.config['MYSQL_DATABASE_PASSWORD'] = '155b1124'
app.config['MYSQL_DATABASE_DB'] = 'heroku_8358d0e5c24233f'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-06.cleardb.net'
mysql.init_app(app)