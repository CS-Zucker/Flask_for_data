from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from models import CommentModel, UserModel, OrderModel, OrderingModel, user_order_rank
from sqlalchemy import func

#一些可视化
bp = Blueprint("view", __name__, url_prefix="/admin/view")
@bp.route('/user_order_rank',methods=['GET','POST'])
def user_order_rank():
    if request.method == 'GET':
        page = request.args.get("page", type=int, default=1)  # 当没有参数时默认为一,转成整形很重要，默认为string
        # 分页器对象
        paginate = UserModel.query.paginate(page=page, per_page=12)  # 当前页和每页展示多少数据
        user_order_rank()
        return 'ok'

        # return render_template("user-order-rank.html", paginate=paginate, user_orders=user_orders )  # 把paginate对象传到前端
    else:
        user_id = request.form.get("userid")  # 要搜索用户id
        if user_id == '':
            return redirect(url_for("operate.user_list"))  # 当没有
        else:
            return redirect(url_for("user-order-rank.html", user_id=user_id))