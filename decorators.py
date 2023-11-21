from functools import wraps
from flask import g, redirect, url_for
def login_required(func):  #需要登录操作就用到这个装饰器
    # 保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:  # 如果用户已经登录了
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))  # 如果用户没有登录就渲染登录界面
    return inner