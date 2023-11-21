from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session,g
from exts import mail, db
from flask_mail import Message
import string
import random
from models import EmailCaptchaModel
from .forms import RegisterForm, LoginForm, PersonalForm
from models import UserModel
from decorators import login_required

bp = Blueprint("auth", __name__, url_prefix="/auth")
#  一些授权操作，如登录和注册
@bp.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)  # 记得把前端form的method改成post
        if form.validate():
            email = form.Email.data
            password = form.Password.data
            user = UserModel.query.filter_by(Email=email).first()  # 查找邮箱
            if not user:  # 邮箱不存在
                print("邮箱不存在")
                return redirect(url_for("auth.login"))
            else:
                if user.Password == password:
                    # cookie用来存放登录授权的信息,cookie在浏览器里存储，这样就知道登录的用户是谁了
                    session['user_id'] = user.UserID
                    return redirect("/")
                else:
                    print("密码错误")
                    return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))  # 登录失败要重新渲染


# get从服务器上获取数据获得渲染的html
# post将客户端数据提交给服务器
# GET 方法将请求参数附加在 URL 中，以查询字符串的形式传递
# 而 POST 方法将请求参数放在请求体中，以表单字段的形式传递
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)  # 获取前端用户提交的form数据扔给registerform进行验证
        if form.validate():  # 调用验证器和验证函数
            userid = form.UserID.data
            email = form.Email.data
            username = form.UserName.data
            password = form.Password.data
            contactnum = form.ContactNumber.data
            user = UserModel(UserID=userid, Email=email, UserName=username, Password=password, ContactNumber= contactnum)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))  # 把视图函数转换成url 蓝图.视图函数
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

@bp.route("/logout")  # 就是把session信息全部清除
def logout():
    session.clear()
    return redirect("/")

# 个人中心
@bp.route("/personal/<string:user_id>", methods=['GET', 'POST'])
def personal(user_id):
    if request.method == 'GET':
        user = UserModel.query.get(user_id)
        return render_template("personal.html", user=user)
    else:
        form = PersonalForm(request.form)  # 获取前端用户提交的form数据扔给registerform进行验证
        if form.validate():  # 调用验证器和验证函数
            userid = user_id
            user = UserModel.query.get(userid)
            user.Email = form.Email.data
            user.UserName = form.UserName.data
            user.Password = form.Password.data
            user.ContactNumber = form.ContactNumber.data
            user.sex = form.sex.data
            db.session.commit()
            return "修改成功"  # 把视图函数转换成url 蓝图.视图函数
        else:
            print(form.errors)
            return redirect(url_for("auth.personal", user_id=g.user.UserID))




# 默认get请求
@bp.route("/captcha/email")  # 获取邮箱生成验证码发送验证码
def get_email_captcha():
    email = request.args.get("email")  # 从HTTP请求的参数中获取名为"email"的参数
    # 产生4位随机数
    source = string.digits*4
    captcha = random.sample(source, 4)  # 随机取4位
    captcha = "".join(captcha)
    message = Message(subject="音乐网站验证码", recipients=[email], body=f"您的验证码是{captcha}")
    mail.send(message)  # 发送验证码
    # 数据库存储验证码
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()  # 提交到数据库
    return jsonify({"code": 200, "message": "", "data": None})  # 返回一个 JSON 格式的 HTTP 响应。表示没有错误，没有错误信息，不需要传输数据


