#encoding: utf-8
# 解决循环引用
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
db = SQLAlchemy()
#ORM层，用于管理Python类和数据库表之间的映射关系。
mail = Mail()