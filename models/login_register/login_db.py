import sys
sys.path.append(r'H:\_gits\Flask_for_data')
from models.sql_db import select_db

def login_judge(user, pwd):
    result = select_db(table='user', res_key='password', search_key='user_name', search_value=user)
    # print(result)   # (result -> tuple)
    msg = ''
    if len(result) != 0:
        if result[0][0] == pwd:
            code = 200
            if user=='admin':
                msg = '管理员账户登录成功'
            else:
                msg = '登录成功'
        else:
            code = 403
            msg = '账号或密码错误'
    else:
        code = 403
        msg = '不存在这个用户'
    return {"code": code, "msg": msg}

