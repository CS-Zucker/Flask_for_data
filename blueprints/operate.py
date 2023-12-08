import os
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from sqlalchemy import or_
from exts import db
from decorators import login_required
from .forms import *
from decorators import login_required
from datetime import datetime
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
            return render_template("search.html")  # 当没有提供歌曲名时给音乐的提示
        song_singers = get_songs(musicname)
        singer = musicname
        singer_songs = get_songs_(singer)
        return render_template("search_result.html",  song_singers=song_singers, singer_songs=singer_songs)  # 把song_singers也传入前端


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




# 显示所有音乐的信息
@bp.route('/music_list',methods=['GET','POST'])
def music_list():
    if request.method == 'GET':
        page = request.args.get("page", type=int, default=1)   # 当没有参数时默认为一,转成整形很重要，默认为string
        # 分页器对象 
        paginate = db.session.query(MusicModel, SingerModel).\
            join(SingingModel, MusicModel.MusicID == SingingModel.MusicID).\
            join(SingerModel, SingerModel.SingerID == SingingModel.SingerID).paginate(page=page, per_page=12)
        
        return render_template("music-list.html", paginate=paginate)  # 把paginate对象传到前端
    else:
        music_id = request.form.get("musicid")  # 要搜索音乐id
        if music_id == '':
            flash("请输入数据")
            return redirect(url_for("operate.music_list"))  # 当没有
        else:
            musics = MusicModel.query.filter(or_(MusicModel.MusicID == music_id, MusicModel.MusicName == music_id))
            if not musics:
                flash("不存在此音乐")
                redirect(url_for("operate.music_list"))
            else:
                return redirect(url_for("operate.music_search", music_id=music_id))


# 删除指定音乐的信息
@bp.route('/music_delete/<string:music_id>')
def music_delete(music_id):
    drop_music = MusicModel.query.get(music_id)  # 删除音乐的id
    db.session.delete(drop_music)
    db.session.commit()
    return redirect(url_for("operate.music_list"))

# 搜索音乐信息
@bp.route('/music_search/<string:music_id>',methods=['GET','POST'])
def music_search(music_id):
    if request.method == 'GET':
        musicid = music_id
        musicname = music_id
        musics = MusicModel.query.filter(or_(MusicModel.MusicID.contains(musicid), MusicModel.MusicName.contains(musicname)))
        return render_template("music-list.html", musics=musics, paginate=None)
    else:
        music_id = request.form.get("musicid")  # 要搜索音乐id
        if music_id == '':
            flash("请输入数据")
            return redirect(url_for("operate.music_list"))  # 当没有
        else:
            return redirect(url_for("operate.music_search", music_id=music_id))
        
# 添加音乐 
@bp.route('/music_add',methods=['GET','POST'])
def music_add():
    if request.method == 'GET':
        return render_template('music-add.html')
    else:
        form = AddMusicForm(request.form)  # 获取前端音乐提交的form数据扔给registerform进行验证
        if form.validate():  # 调用验证器和验证函数
            musicf = request.files['musicfile']
            coverf = request.files['coverfile']
            musicf.save(os.path.join("static/musics/", musicf.filename))
            coverf.save(os.path.join("static/images/", coverf.filename))

            musicid = form.MusicID.data
            musicname = form.MusicName.data
            intro = form.Intro.data
            classid = form.ClassID.data
            price = form.price.data
            issuetime = form.IssueTime.data
            storagelocation = os.path.join(musicf.filename)
            coverlocation = os.path.join(coverf.filename)[:4]
            
            singerid = form.SingerID.data
            singername = form.Singer.data
            singersex = form.SingerSex.data
            
            music = MusicModel(MusicID=musicid, MusicName=musicname, ClassID=classid, Intro=intro, price=price, IssueTime=issuetime, StorageLocation=storagelocation, Cover=coverlocation)
            singer = SingerModel(SingerID=singerid, Singer=singername, SingerSex=singersex)
            singing = SingingModel(SingerID=singerid, MusicID=musicid)
            db.session.add(music)
            db.session.add(singer)
            db.session.add(singing)
            db.session.commit()
            flash("音乐添加成功！")  # 添加Flash消息
            return redirect(url_for("operate.music_list"))  # 把视图函数转换成url 蓝图.视图函数
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'错误：{error} ')
            return redirect(url_for("operate.music_add"))

# 修改音乐信息 
@bp.route('/music_edit/<string:music_id>?<string:singer_id>',methods=['GET','POST'])
def music_edit(music_id, singer_id):
    if request.method == 'GET':
        return render_template('music-edit.html')
    else:
        form = EditMusicForm(request.form)  # 获取前端音乐提交的form数据扔给registerform进行验证
        if form.validate():  # 调用验证器和验证函数
            musicf = request.files['musicfile']
            coverf = request.files['coverfile']
            musicf.save(os.path.join("static/musics/", musicf.filename))
            coverf.save(os.path.join("static/images/", coverf.filename))

            music = MusicModel.query.get(music_id)
            music.MusicName = form.MusicName.data
            music.Intro = form.Intro.data
            music.ClassID = form.ClassID.data
            music.price = form.price.data
            music.IssueTime = form.IssueTime.data
            
            singer = SingerModel.query.get(singer_id)
            singer.Singer = form.Singer.data
            singer.SingerSex = form.SingerSex.data
            
            music.StorageLocation = os.path.join(musicf.filename)
            music.Cover = os.path.join(coverf.filename)[:4]
            db.session.commit()
            flash("音乐修改成功！")  # 添加Flash消息
            return redirect(url_for("operate.music_list"))  # 把视图函数转换成url 蓝图.视图函数
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'错误：{error} ')
            print(form.errors)
            return redirect(url_for("operate.music_edit", music_id=music_id))




@bp.route('/comment_list',methods=['GET','POST'])
def comment_list():
    if request.method == 'GET':
        page = request.args.get("page", type=int, default=1)   # 当没有参数时默认为一,转成整形很重要，默认为string

        paginate = CommentModel.query.paginate(page=page, per_page=10)

        # 从UserModel中提取music_id和user_id
        user_ids = [comment.UserID for comment in paginate.items]
        music_ids = [comment.MusicID for comment in paginate.items]
        contents = [comment.Content for comment in paginate.items]
        comment_ids = [comment.CommentID for comment in paginate.items]
        comment_times = [comment.CommentTime for comment in paginate.items]

        # 查询MusicModel和UserModel，获取对应的musicname和username
        music_names = MusicModel.query.filter(MusicModel.MusicID.in_(music_ids)).all()
        user_names = UserModel.query.filter(UserModel.UserID.in_(user_ids)).all()

        # 创建字典以便于在模板中使用
        comment_data = {}
        for comment in paginate.items:
            comment_data[comment.CommentID] = {
                'music_id': comment.MusicID,
                'user_id': comment.UserID,
                'content': comment.Content,
                'comment_id': comment.CommentID,
                'comment_time':comment.CommentTime,
                'music_name': next((music.MusicName for music in music_names if music.MusicID == comment.MusicID), None),
                'user_name': next((user.UserName for user in user_names if user.UserID == comment.UserID), None),
                # 添加其他评论相关信息
            }

        return render_template("comment_list.html", paginate=paginate,comment_datas=comment_data)  # 把paginate对象传到前端
    else:
        user_id = request.form.get("userid")
        music_name = request.form.get("musicname")
        comment_content = request.form.get("commentcontent")
        if user_id:
            return redirect(url_for("operate.comment_user_search", username=user_id))
        elif music_name:
            return redirect(url_for("operate.comment_music_search", musicname=music_name))

        elif comment_content:
            return redirect(url_for("operate.comment_comment_search", comment=comment_content))
        else:
            return redirect(url_for("operate.comment_list"))


@bp.route('/comment_delete/<string:comment_id>')
def comment_delete(comment_id):
    comment = CommentModel.query.get(comment_id)  # 获取评论
    if comment:
        deleted_comment_id = comment.CommentID  # 保存要删除的评论ID
        db.session.delete(comment)  # 删除评论


        # 更新比被删除评论ID大的其他评论的ID
        CommentModel.query.filter(CommentModel.CommentID > deleted_comment_id).update(
            {CommentModel.CommentID: CommentModel.CommentID - 1},
            synchronize_session=False
        )
        db.session.commit()

    return redirect(url_for("operate.comment_list"))

@bp.route('/comment_user_search/<string:username>',methods=['GET','POST'])
def comment_user_search(username):
    if request.method == 'GET':
        page = request.args.get("page", type=int, default=1)  # 当没有参数时默认为一,转成整形很重要，默认为string
        # 分页器对象
        user = UserModel.query.filter( UserModel.UserName == username).first()

        if user:
         paginate = CommentModel.query.filter(CommentModel.UserID == user.UserID).paginate(page=page, per_page=10)
         user_ids = [comment.UserID for comment in paginate.items]
         music_ids = [comment.MusicID for comment in paginate.items]
         contents = [comment.Content for comment in paginate.items]
         comment_ids = [comment.CommentID for comment in paginate.items]
         comment_times = [comment.CommentTime for comment in paginate.items]

        # 查询MusicModel和UserModel，获取对应的musicname和username
         music_names = MusicModel.query.filter(MusicModel.MusicID.in_(music_ids)).all()
         user_names = UserModel.query.filter(UserModel.UserID.in_(user_ids)).all()

        # 创建字典以便于在模板中使用
         comment_data = {}
         for comment in paginate.items:
            comment_data[comment.CommentID] = {
                'music_id': comment.MusicID,
                'user_id': comment.UserID,
                'content': comment.Content,
                'comment_id': comment.CommentID,
                'comment_time': comment.CommentTime,
                'music_name': next((music.MusicName for music in music_names if music.MusicID == comment.MusicID),
                                   None),
                'user_name': next((user.UserName for user in user_names if user.UserID == comment.UserID), None),
                # 添加其他评论相关信息
            }

         return render_template("comment_list.html", paginate=paginate, comment_datas=comment_data)  # 把paginate对象传到前端
        else:
            # 处理找不到用户的情况
            flash('找不到指定用户名的用户。')
            return redirect(url_for('operate.comment_list'))
    else:
        user_id = request.form.get("userid")
        music_name = request.form.get("musicname")
        comment_content = request.form.get("commentcontent")
        if user_id:
            return redirect(url_for("operate.comment_user_search", username=user_id))
        elif music_name:

            return redirect(url_for("operate.comment_music_search", musicname=music_name))

        elif comment_content:

            return redirect(url_for("operate.comment_comment_search", comment=comment_content))
        else:
            return redirect(url_for("operate.comment_list"))
@bp.route('/comment_music_search/<string:musicname>',methods=['GET','POST'])
def comment_music_search(musicname):
    if request.method == 'GET':
        page = request.args.get("page", type=int, default=1)  # 当没有参数时默认为一,转成整形很重要，默认为string
        # 分页器对象
        music = MusicModel.query.filter( MusicModel.MusicName == musicname).first()

        if music:
         paginate = CommentModel.query.filter(CommentModel.MusicID == music.MusicID).paginate(page=page, per_page=10)
         user_ids = [comment.UserID for comment in paginate.items]
         music_ids = [comment.MusicID for comment in paginate.items]
         contents = [comment.Content for comment in paginate.items]
         comment_ids = [comment.CommentID for comment in paginate.items]
         comment_times = [comment.CommentTime for comment in paginate.items]

        # 查询MusicModel和UserModel，获取对应的musicname和username
         music_names = MusicModel.query.filter(MusicModel.MusicID.in_(music_ids)).all()
         user_names = UserModel.query.filter(UserModel.UserID.in_(user_ids)).all()

        # 创建字典以便于在模板中使用
         comment_data = {}
         for comment in paginate.items:
            comment_data[comment.CommentID] = {
                'music_id': comment.MusicID,
                'user_id': comment.UserID,
                'content': comment.Content,
                'comment_id': comment.CommentID,
                'comment_time': comment.CommentTime,
                'music_name': next((music.MusicName for music in music_names if music.MusicID == comment.MusicID),
                                   None),
                'user_name': next((user.UserName for user in user_names if user.UserID == comment.UserID), None),
                # 添加其他评论相关信息
            }

         return render_template("comment_list.html", paginate=paginate, comment_datas=comment_data)  # 把paginate对象传到前端
        else:
            # 处理找不到用户的情况
            flash('找不到指定音乐名的音乐。')
            return redirect(url_for('operate.comment_list'))
    else:
        user_id = request.form.get("userid")
        music_name = request.form.get("musicname")
        comment_content = request.form.get("commentcontent")
        if user_id:
            return redirect(url_for("operate.comment_user_search", username=user_id))
        elif music_name:
            return redirect(url_for("operate.comment_music_search", musicname=music_name))

        elif comment_content:
            return redirect(url_for("operate.comment_comment_search", comment=comment_content))
        else:
            return redirect(url_for("operate.comment_list"))

@bp.route('/comment_comment_search/<string:comment>',methods=['GET','POST'])
def comment_comment_search(comment):
    if request.method == 'GET':
        page = request.args.get("page", type=int, default=1)  # 当没有参数时默认为一,转成整形很重要，默认为string
        # 分页器对象
        com = CommentModel.query.filter(CommentModel.Content == comment).first()

        if com:
         paginate = CommentModel.query.filter(func.trim(CommentModel.Content) == com.Content).paginate(page=page, per_page=10)
         user_ids = [comment.UserID for comment in paginate.items]
         music_ids = [comment.MusicID for comment in paginate.items]
         contents = [comment.Content for comment in paginate.items]
         comment_ids = [comment.CommentID for comment in paginate.items]
         comment_times = [comment.CommentTime for comment in paginate.items]

        # 查询MusicModel和UserModel，获取对应的musicname和username
         music_names = MusicModel.query.filter(MusicModel.MusicID.in_(music_ids)).all()
         user_names = UserModel.query.filter(UserModel.UserID.in_(user_ids)).all()

        # 创建字典以便于在模板中使用
         comment_data = {}
         for comment in paginate.items:
            comment_data[comment.CommentID] = {
                'music_id': comment.MusicID,
                'user_id': comment.UserID,
                'content': comment.Content,
                'comment_id': comment.CommentID,
                'comment_time': comment.CommentTime,
                'music_name': next((music.MusicName for music in music_names if music.MusicID == comment.MusicID),
                                   None),
                'user_name': next((user.UserName for user in user_names if user.UserID == comment.UserID), None),
                # 添加其他评论相关信息
            }

         return render_template("comment_list.html", paginate=paginate, comment_datas=comment_data)  # 把paginate对象传到前端
        else:
            # 处理找不到用户的情况
            flash('找不到指定内容的评论。')
            return redirect(url_for('operate.comment_list'))
    else:
        user_id = request.form.get("userid")
        music_name = request.form.get("musicname")
        comment_content = request.form.get("commentcontent")
        if user_id:
            return redirect(url_for("operate.comment_user_search", username=user_id))
        elif music_name:

            return redirect(url_for("operate.comment_music_search", musicname=music_name))

        elif comment_content:

            return redirect(url_for("operate.comment_comment_search", comment=comment_content))
        else:
            return redirect(url_for("operate.comment_list"))

@bp.route('/ad_list')
def ad_list():
    page = request.args.get('page', 1, type=int)
    paginate = AdvertisingID.query.paginate(page=page, per_page=10)
    return render_template('ad_list.html', paginate=paginate)

@bp.route('/ad_add', methods=['GET', 'POST'])
def ad_add():
    if request.method == 'POST':
        title = request.form['title']
        abstract = request.form['abstract']
        content = request.form['content']
        picture = request.form['picture']
        release_time = datetime.utcnow()
        new_ad = AdvertisingID(title=title, Abstract=abstract, content=content, Picture=picture,ReleaseTime=release_time)
        db.session.add(new_ad)
        db.session.commit()

        flash('广告添加成功', 'success')
        return redirect(url_for('operate.ad_list'))

    return render_template('ad_add.html')

@bp.route('/ad_delete/<int:ad_id>')
def ad_delete(ad_id):
    ad =AdvertisingID.query.get_or_404(ad_id)
    db.session.delete(ad)
    db.session.commit()

    flash('广告删除成功', 'success')
    return redirect(url_for('operate.ad_list'))

@bp.route('/save_comment/<int:music_id>', methods=['POST'])
@login_required
def save_comment(music_id):
    form = AddCommentForm(request.form)  # 获取前端用户提交的form数据扔给registerform进行验证
    content = form.Content.data
    print(content)
    if form.validate():  # 调用验证器和验证函数
        content = form.Content.data
        print(content)
        # 查询数据库中的评论数量
        comment_count = CommentModel.query.count()
        time = datetime.utcnow()
        # 生成新评论的 CommentID
        new_comment_id = comment_count + 1
        # 创建新评论
        new_comment = CommentModel(CommentID=new_comment_id, Content=content, CommentTime=time, MusicID=music_id,
                                   UserID=g.user.UserID)
        # 添加到数据库并提交
        db.session.add(new_comment)
        db.session.commit()
        flash("评论添加成功！")  # 添加Flash消息
        return redirect(url_for("music.single", id=music_id))  # 把视图函数转换成url 蓝图.视图函数
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'错误：{error} ')
        return redirect(url_for("music.single",id=music_id))
    
@bp.route('/create_order/<int:music_id>', methods=['POST'])
@login_required
def create_order(music_id):
    # 查询数据库中的订单数量
    order_count = OrderModel.query.count()
    time = datetime.utcnow()
    # 生成新订单的 OrderID
    new_order_id = order_count + 1
    # 创建新订单
    new_order = OrderModel(OrderID=new_order_id, UserID=g.user.UserID, OrderTime=time, DownloadStatus='1')
    new_ordering = OrderingModel(OrderID=new_order_id, MusicID=music_id)
    # 添加到数据库并提交
    db.session.add(new_order)
    db.session.add(new_ordering)
    db.session.commit()
    flash("订单添加成功！")  # 添加Flash消息
    return redirect(url_for("music.single", id=music_id))  # 把视图函数转换成url 蓝图.视图函数


# 显示所有订单的信息
@bp.route('/order_list',methods=['GET','POST'])
def order_list():
    if request.method == 'GET':
        page = request.args.get("page", type=int, default=1)   # 当没有参数时默认为一,转成整形很重要，默认为string
        # 分页器对象
        paginate = OrderModel.query.paginate(page=page, per_page=12)  # 当前页和每页展示多少数据

        return render_template("order-list.html", paginate=paginate,)  # 把paginate对象传到前端
    else:
        order_id = request.form.get("orderid")  # 要搜索订单id
        if order_id == '':
            flash("请输入数据")
            return redirect(url_for("operate.order_list"))  # 当没有
        else:
            orders = OrderModel.query.filter(or_(OrderModel.OrderID == order_id, OrderModel.UserID == order_id))
            if not orders:
                flash("不存在此订单")
                redirect(url_for("operate.order_list"))
            else:
                return redirect(url_for("operate.order_search", order_id=order_id))


# 搜索订单信息
@bp.route('/order_search/<string:order_id>',methods=['GET','POST'])
def order_search(order_id):
    if request.method == 'GET':
        orderid = order_id
        userid = order_id
        orders = OrderModel.query.filter(or_(OrderModel.OrderID.contains(orderid), OrderModel.UserID.contains(userid)))
        return render_template("order-list.html", orders=orders, paginate=None)
    else:
        order_id = request.form.get("orderid")  # 要搜索订单id
        if order_id == '':
            flash("请输入数据")
            return redirect(url_for("operate.order_list"))  # 当没有
        else:
            return redirect(url_for("operate.order_search", order_id=order_id))

# 删除指定订单的信息
@bp.route('/order_delete/<string:order_id>')
def order_delete(order_id):
    drop_order = OrderModel.query.get(order_id)  # 删除订单的id
    db.session.delete(drop_order)
    db.session.commit()
    return redirect(url_for("operate.order_list"))