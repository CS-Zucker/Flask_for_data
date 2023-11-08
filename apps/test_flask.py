from flask import Flask, render_template, request, flash,  jsonify, redirect, url_for, session
import json
import time
import os
from flask_cors import CORS

import sys
sys.path.append(r'H:\_gits\Flask_for_data')
from models.sql_db import insert_db, select_db
from models.login_register import login_judge, register_judge

# 创建flask对象
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config['SECRET_KEY'] = 'qwert asdfg zxcvb'
CORS(app,supports_credentials=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='GET':
        return render_template('demo_login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register_api():
    if request.method=='GET':
        return render_template('demo_login.html')
    else:
        name_form = request.form.get('user_name')
        email_form = request.form.get('user_email')
        pwd_form = request.form.get('user_pwd')

        res_dic = register_judge(name=name_form, email=email_form, pwd=pwd_form)
        res_msg = res_dic['msg']
        return render_template('demo_login.html', error_msg=str(res_msg))


@app.route('/login', methods=['GET', 'POST'])
def login_api():
    if request.method == 'GET':
        return render_template('demo_login.html')
    else:
        user_form = request.form.get('user')
        pwd_form = request.form.get('pwd')
        print('用户名:',user_form,'  密码:',pwd_form)

        res_dic = login_judge(user=user_form, pwd=pwd_form)
        res_msg = res_dic['msg']
        res_code = res_dic['code']
        print(res_msg)
        if res_code==200 :
            session['user'] = user_form
            session.permanent = True
            if user_form=='admin' :
                return redirect(url_for('test'))
            return redirect(url_for('test'))
        return render_template('demo_login.html', error_msg=str(res_msg))
    




@app.route('/test', methods=['GET', 'POST'])
def test():
    """
    功能(个人中心界面): 根据"stu_id"从数据库中得到学生基本信息，用于个人中心信息显示
    :return:
    """
    user_id = session.get('user')
    print(user_id)
    result = user_id
    return render_template('index.html', result=result)


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


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)
