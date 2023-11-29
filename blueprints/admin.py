from flask import Blueprint, render_template, request, redirect, url_for, session,g

from .forms import *
from exts import db
from models import *


# 管理员首页
bp = Blueprint("admin", __name__, url_prefix="/admin")
@bp.route('/')
def admin_home():
    return redirect(url_for("admin.admin_index"))

@bp.route("/index")  # 就是把session信息全部清除
def admin_index():
    return render_template("admin_index.html")

#  一些授权操作，如登录和注册
@bp.route("/login", methods=['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template("admin_login.html")
    else:
        form = AdminForm(request.form)  # 记得把前端form的method改成post
        if form.validate():
            adminID = form.AdminId.data
            password = form.Password.data
            admin = Admin.query.filter_by(AdminID=adminID).first()  # 查找AdminID
            if not admin:  # 管理员不存在
                print("管理员不存在")
                return redirect(url_for("admin.admin_login"))
            else:
                if admin.Password == password:
                    # cookie用来存放登录授权的信息,cookie在浏览器里存储，这样就知道登录的用户是谁了
                    session['admin_id'] = admin.AdminID
                    return redirect(url_for("admin.admin_index"))
                else:
                    print("密码错误")
                    return redirect(url_for("admin.admin_login"))
        else:
            print(form.errors)
            return redirect(url_for("admin.admin_login"))  # 登录失败要重新渲染

