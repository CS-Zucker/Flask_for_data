from flask import Blueprint, render_template, request
from models import *
import random

bp = Blueprint("music", __name__, url_prefix="/")

@bp.route('/')
def index():
    songs = MusicModel.query.all()
    ads = AdvertisingID.query.all()
    classes = ClassModel.query.all()
    songs_by_class = {}
    # Randomly select one ad
    random_ad = random.choice(ads) if ads else None
    for c in classes:
        songs_of_class = [song for song in songs if song.ClassID == c.ClassID]
        songs_by_class[c.TypeName] = songs_of_class

    return render_template('library.html', songs_by_class=songs_by_class, ad=random_ad,cl=classes)

@bp.route('/chart', methods=['GET', 'POST'])
def chart(): 
    # 执行查询
    chart_music_dict = get_songs_for_chart()
    return render_template('chart.html', chart_music_dict=chart_music_dict)

@bp.route('/single/<int:id>')
def single(id):
    song = MusicModel.query.get(id)
    singing_entry = SingingModel.query.filter_by(MusicID=id).first()
    if singing_entry:
        singer_id = singing_entry.SingerID
        # 根据歌手ID查询歌手信息
        singer = SingerModel.query.get(singer_id)
    else:
        singer = None

    base_path = "../static/musics/"
    audio_url = base_path + song.StorageLocation
    #user = {'id': session.get('user_id'), 'username': session.get('username')}
    return render_template('single.html', song=song, singer=singer,audio_url=audio_url,musicid=id)

