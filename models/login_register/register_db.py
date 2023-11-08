import sys
sys.path.append(r'H:\_gits\Flask_for_data')
from models.sql_db import select_db, insert_db

def register_judge(name, email, pwd):
    res_exist_name = select_db(table='user', res_key='COUNT(*)', search_key='user_name', search_value=name)
    res_exist_email = select_db(table='user', res_key='COUNT(*)', search_key='user_email', search_value=email)
    msg = ''
    code = 403
    if res_exist_name[0][0] != 0:
        msg += '该用户名已注册\n'
    if res_exist_email[0][0] != 0:
        msg += '该邮箱已注册\n'
    if msg == '':
        insert_keys = ','.join(['user_name', 'password', 'user_email'])
        insert_values = ', '.join(["'" + x + "'" for x in [name, pwd, email]])
        res_insert = insert_db(table='user', key=insert_keys, value=insert_values)
        if res_insert == True:
            code = 200
            msg = '注册成功，请登录'
    return {"code": code, "msg": msg}