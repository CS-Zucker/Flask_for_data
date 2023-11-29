from flask import Blueprint,request, render_template,flash,redirect,url_for
from sqlalchemy import text
#一些可视化
from exts import engine
bp = Blueprint("view", __name__, url_prefix="/admin/view")
@bp.route('/user_order_rank',methods=['GET','POST'])
def user_order_rank():
    if request.method == 'GET':
        user_order_rank = text("""
        SELECT u.UserID,u.UserName,u.MusicName,us.OrderCount
        FROM userorder_view AS u,user_order_rankview AS us
        WHERE u.UserID = us.UserID
        ORDER BY       
            OrderCount DESC;
        """)
        with engine.connect() as conn:
            result = conn.execute(user_order_rank).fetchall()  # 执行sql
        # for row in result:
        #     print("UserID: ", row.UserID)
        #     print("UserName: ", row.UserName)
        #     print("MusicName: ", row.MusicName)
        #     print("OrderCount: ", row.OrderCount)
        #     print()
        return render_template('user-order-rank.html',result=result)
    else:
        user_id = request.form.get("userid")  # 要搜索用户id
        if user_id == '':
            flash("请输入数据")
            return redirect(url_for("view.user_order_rank"))  # 当没有
        else:
            user_order_rank_search = text("""
                    SELECT u.UserID,u.UserName,u.MusicName,us.OrderCount
                    FROM userorder_view AS u,user_order_rankview AS us
                    WHERE u.UserID = us.UserID AND u.UserID =:userid;
                    """)
            with engine.connect() as conn:
                result_ = conn.execute(user_order_rank_search, {"userid": user_id}).fetchall()  # 执行sql
            if not result_:
                flash("不存在此用户")
                user_order_rank = text("""
                       SELECT u.UserID,u.UserName,u.MusicName,us.OrderCount
                       FROM userorder_view AS u,user_order_rankview AS us
                       WHERE u.UserID = us.UserID
                       ORDER BY       
                           OrderCount DESC;
                       """)
                with engine.connect() as conn:
                    result = conn.execute(user_order_rank).fetchall()  # 执行sql
                    return render_template('user-order-rank.html', result=result)
            else:
                return render_template('user-order-rank.html', result=result_)
@bp.route('/song_sales',methods=['GET','POST'])
def song_sales():
    if request.method == 'GET':
        user_order_rank = text("""
        SELECT u.UserID,u.UserName,u.MusicName,us.OrderCount
        FROM userorder_view AS u,user_order_rankview AS us
        WHERE u.UserID = us.UserID
        ORDER BY       
            OrderCount DESC;
        """)
        with engine.connect() as conn:
            result = conn.execute(user_order_rank).fetchall()  # 执行sql
        return render_template('user-order-rank.html',result=result)
    else:
        user_id = request.form.get("userid")  # 要搜索用户id
        if user_id == '':
            flash("请输入数据")
            return redirect(url_for("view.user_order_rank"))  # 当没有
        else:
            user_order_rank_search = text("""
                    SELECT u.UserID,u.UserName,u.MusicName,us.OrderCount
                    FROM userorder_view AS u,user_order_rankview AS us
                    WHERE u.UserID = us.UserID AND u.UserID =:userid;
                    """)
            with engine.connect() as conn:
                result_ = conn.execute(user_order_rank_search, {"userid": user_id}).fetchall()  # 执行sql
            if not result_:
                flash("不存在此用户")
                user_order_rank = text("""
                       SELECT u.UserID,u.UserName,u.MusicName,us.OrderCount
                       FROM userorder_view AS u,user_order_rankview AS us
                       WHERE u.UserID = us.UserID
                       ORDER BY       
                           OrderCount DESC;
                       """)
                with engine.connect() as conn:
                    result = conn.execute(user_order_rank).fetchall()  # 执行sql
                    return render_template('user-order-rank.html', result=result)
            else:
                return render_template('user-order-rank.html', result=result_)