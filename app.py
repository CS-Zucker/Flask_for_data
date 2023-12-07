from flask import Flask, session, g, render_template, jsonify, request
from exts import db, mail
import config
from datetime import datetime
from models import UserModel
from flask_migrate import Migrate
from blueprints.auth import bp as auth_bp
from blueprints.music import bp as music_bp
from blueprints.operate import bp as operate_bp
from blueprints.admin import bp as admin_bp
from blueprints.view import bp as view_bp
from models import CommentModel
app = Flask(__name__)
app.config.from_object(config)  # 绑定配置文件
# 与db绑定
db.init_app(app)  # 告诉 Flask，我们的应用将使用 Flask-SQLAlchemy 来管理数据库


mail.init_app(app)  # 设置 Flask-Mail，这个扩展用于发送邮件
migrate = Migrate(app, db)  # 初始化 Flask-Migrate。Flask-Migrate 是一个用于 Flask 的数据库迁移扩展
app.register_blueprint(auth_bp)  # 注册蓝图（Blueprints）
app.register_blueprint(music_bp)
app.register_blueprint(operate_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(view_bp)
app.secret_key='meng'  # 加密闪现消息
@app.before_request
def my_before_request():  # 钩子函数
    user_id = session.get("user_id")
    if user_id:  # 用户已经登录
        user = UserModel.query.get(user_id)  # 获得用户
        setattr(g, "user", user)  # 把uer设为全局变量
    else:
        setattr(g, "user", None)

@app.context_processor  # 上下文处理器
def my_context_processor():
    return {"user": g.user}


# #############################  异常处理  ###########################
# 403错误
@app.errorhandler(403)
def handle_403_miss(e):
    return render_template('error-403.html'), 403


# 404错误
@app.errorhandler(404)
def handle_404_error(e):
     return render_template('error-404.html'), 404


# 405错误
@app.errorhandler(405)
def handle_405_error(e):
    return render_template('error-405.html'), 405


# 500错误
@app.errorhandler(500)
def handle_500_error(e):
    return render_template('error-500.html'), 500



@app.route('/get_comments/<int:music_id>')
def get_comments(music_id):
    try:
        # 查询特定歌曲的评论
        comments = CommentModel.query.filter_by(MusicID=music_id).all()

        # 将评论转换为字典列表，包含用户名
        comments_dict_list = [
            {
                'id': comment.CommentID,
                'content': comment.Content,
                'time': comment.CommentTime.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': comment.UserID,
                'username': get_username_by_user_id(comment.UserID)
            }
            for comment in comments
        ]

        return jsonify({'status': 'success', 'comments': comments_dict_list})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def get_username_by_user_id(user_id):
    try:
        # 查询用户模型，获取用户名
        user = UserModel.query.filter_by(UserID=user_id).first()
        if user:
            return user.UserName  # 使用正确的字段名
        else:
            return 'Unknown User'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)