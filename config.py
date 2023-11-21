
SECRET_KEY = 'mengzhuoya'  # 用来加密cookie
# 数据库配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'music__'
USERNAME = 'root'
PASSWORD = 'm2003z07y02?'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "1943583024@qq.com"
MAIL_PASSWORD = "dhanooikbtkadjib"
MAIL_DEFAULT_SENDER = "1943583024@qq.com"
