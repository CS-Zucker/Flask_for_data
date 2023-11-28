from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from sqlalchemy import or_
from exts import db
from models import CommentModel, UserModel, OrderModel, OrderingModel
from models import get_songs, get_songs_
from .forms import AddUserForm, EditUserForm
from decorators import login_required
bp = Blueprint("operate", __name__, url_prefix="/operate")
# 定义用一些操作

# 搜索歌曲功能
@bp.route("/search", methods=['GET','POST'])
def search():
    if request.method == 'GET':
        return render_template("search.html")
    else:
        musicname = request.form.get("m")  # 要搜索的歌曲
        if musicname is None:
            flash('请输入歌曲或歌手名称')
            return render_template("search.html")  # 当没有提供歌曲名时给用户的提示
        song_singers = get_songs(musicname)
        singer = musicname
        singer_songs = get_songs_(singer)
        return render_template("search_result.html",  song_singers=song_singers, singer_songs=singer_songs)  # 把song_singers也传入前端

# 评论
@bp.route('/save_comment', methods=['POST'])
def save_comment():
    try:
        # 从JSON请求中获取评论文本
        data = request.get_json()
        text = data.get('text', '')

        if text:
            # 创建 Comment 对象并保存到数据库
            new_comment = CommentModel(Content=text)
            db.session.add(new_comment)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Comment text is empty'})

    except Exception as e:
        # 处理可能出现的错误
        return jsonify({'status': 'error', 'message': str(e)})

# 显示所有用户的信息
@bp.route('/user_list',methods=['GET','POST'])
def user_list():
    if request.method == 'GET':
        page = request.args.get("page", type=int, default=1)   # 当没有参数时默认为一,转成整形很重要，默认为string
        # 分页器对象
        paginate = UserModel.query.paginate(page=page, per_page=12)  # 当前页和每页展示多少数据

        return render_template("user-list.html", paginate=paginate,)  # 把paginate对象传到前端
    else:
        user_id = request.form.get("userid")  # 要搜索用户id
        if user_id == '':
            flash("请输入数据")
            return redirect(url_for("operate.user_list"))  # 当没有
        else:
            users = UserModel.query.filter(or_(UserModel.UserID == user_id, UserModel.UserName == user_id))
            if not users:
                flash("不存在此用户")
                redirect(url_for("operate.user_list"))
            else:
                return redirect(url_for("operate.user_search", user_id=user_id))

# 删除指定用户的信息
@bp.route('/user_delete/<string:user_id>')
def user_delete(user_id):
    orders = OrderModel.query.filter_by(UserID=user_id).all()  # 订单
    for order in orders:
        ordering = OrderingModel.query.filter_by(OrderID=order.OrderID).all()  # 先删除下单
        for item in ordering:
            db.session.delete(item)
        db.session.commit()
        db.session.delete(order)   # 再删除订单
        db.session.commit()
    user = UserModel.query.get(user_id)  # 最后删除用户
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("operate.user_list"))

@bp.route('/user_search/<string:user_id>',methods=['GET','POST'])
def user_search(user_id):
    if request.method == 'GET':
        userid = user_id
        username = user_id
        users = UserModel.query.filter(or_(UserModel.UserID.contains(userid), UserModel.UserName.contains(username)))
        return render_template("user-list.html", users=users, paginate=None)
    else:
        user_id = request.form.get("userid")  # 要搜索用户id
        if user_id == '':
            flash("请输入数据")
            return redirect(url_for("operate.user_list"))  # 当没有
        else:
            return redirect(url_for("operate.user_search", user_id=user_id))
# 添加用户
@bp.route('/user_add',methods=['GET','POST'])
def user_add():
    if request.method == 'GET':
        return render_template('user-add.html')
    else:
        form = AddUserForm(request.form)  # 获取前端用户提交的form数据扔给registerform进行验证
        if form.validate():  # 调用验证器和验证函数
            userid = form.UserID.data
            email = form.Email.data
            username = form.UserName.data
            password = form.Password.data
            contactnum = form.ContactNumber.data
            user = UserModel(UserID=userid, Email=email, UserName=username, Password=password, ContactNumber=contactnum)
            db.session.add(user)
            db.session.commit()
            flash("用户添加成功！")  # 添加Flash消息
            return redirect(url_for("operate.user_list"))  # 把视图函数转换成url 蓝图.视图函数
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'错误：{error} ')
            return redirect(url_for("operate.user_add"))

@bp.route('/user_edit/<string:user_id>',methods=['GET','POST'])
def user_edit(user_id):
    if request.method == 'GET':
        return render_template('user-edit.html')
    else:
        form = EditUserForm(request.form)  # 获取前端用户提交的form数据扔给registerform进行验证
        if form.validate():  # 调用验证器和验证函数
            userid = user_id
            user = UserModel.query.get(userid)
            user.Email = form.Email.data
            user.UserName = form.UserName.data
            db.session.commit()
            flash("用户信息修改成功！")  # 添加Flash消息
            return redirect(url_for("operate.user_list"))  # 把视图函数转换成url 蓝图.视图函数
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'错误：{error} ')
            print(form.errors)
            return redirect(url_for("operate.user_edit", user_id=user_id))



