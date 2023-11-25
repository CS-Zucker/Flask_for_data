from flask import Blueprint, render_template



# 管理员首页
bp = Blueprint("admin", __name__, url_prefix="/admin")
@bp.route('/')
def admin_index():
    return render_template('admin_index.html')