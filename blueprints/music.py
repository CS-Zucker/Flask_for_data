from flask import Blueprint, render_template, request
from models import *
from decorators import login_required
from flask_json import jsonify
import datetime
bp = Blueprint("music", __name__, url_prefix="/")

@bp.route('/')
def index():
    musics = MusicModel.query.all()

    return render_template('library.html', songs=musics)

@bp.route('/chart', methods=['GET', 'POST'])
def chart(): 
    # 执行查询
    chart_music_dict = get_songs_for_chart()
    return render_template('chart.html', chart_music_dict=chart_music_dict)

#  播放歌曲
@bp.route('/single/<int:id>')
def single(id):
    song = MusicModel.query.get(id)
    audio_url = song.StorageLocation
    return render_template('single.html', song=song, audio_url=audio_url)

@bp.route('/save_comment', methods=['GET','POST'])
@login_required
def save_comment():
    if request.method == 'GET':
        return render_template("library.html")
    else:
        try:
            data = request.get_json()

            text = data.get('text')
            created_at_str = data.get('created_at')
            created_at = datetime.fromisoformat(created_at_str)
            music_id = data.get('musicId')

            if text:
                # 查询数据库中的评论数量
                comment_count = CommentModel.query.count()

                # 生成新评论的 CommentID
                new_comment_id = comment_count + 1

                # 创建新评论
                new_comment = CommentModel(CommentID=new_comment_id, Content=text, CommentTime=created_at, MusicID=music_id,
                                           UserID=1)

                # 添加到数据库并提交
                db.session.add(new_comment)
                db.session.commit()
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'error', 'message': 'Comment text is empty'})

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})