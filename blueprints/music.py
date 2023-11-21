from flask import Blueprint, render_template
from models import MusicModel
bp = Blueprint("music", __name__, url_prefix="/")

@bp.route('/')
def index():
    musics = MusicModel.query.all()

    return render_template('library.html', songs=musics)

#  播放歌曲
@bp.route('/single/<int:id>')
def single(id):
    song = MusicModel.query.get(id)
    audio_url = song.StorageLocation
    return render_template('single.html', song=song, audio_url=audio_url)