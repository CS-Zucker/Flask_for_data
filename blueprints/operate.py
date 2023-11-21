from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
import string
from sqlalchemy.orm import joinedload
from exts import db
from models import CommentModel
from models import get_songs
bp = Blueprint("operate", __name__, url_prefix="/operate")
# 定义用户的一些操作
@bp.route("/search", methods=['GET','POST'])  #搜索功能
def search():
    if request.method == 'GET':
        return render_template("search.html")
    else:
        musicname = request.form.get("m")  # 要搜索的歌曲
        if musicname is None:
            return render_template("search.html") # 当没有提供歌曲名时给用户的提示
        song_singers = get_songs(musicname)
        return render_template("search_result.html",  song_singers=song_singers)  # 把song_singers也传入前端

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