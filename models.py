
from exts import db

class UserModel(db.Model):
    __tablename__ = "用户"
    UserID = db.Column(db.String(11), primary_key=True)
    Password = db.Column(db.String(30), nullable=False)
    UserName = db.Column(db.String(20))
    sex = db.Column(db.Enum("男", "女"),nullable=True)
    Email = db.Column(db.String(50), nullable=False)
    ContactNumber = db.Column(db.String(11), nullable=False)

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    captcha = db.Column(db.String(6), nullable=False)

class ClassModel(db.Model):
    __tablename__ = '类型'
    ClassID = db.Column(db.Integer, primary_key=True, nullable=False)
    TypeName = db.Column(db.String(100), nullable=False)

class MusicModel(db.Model):
    __tablename__ = '音乐'

    MusicID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, db.ForeignKey('类型.ClassID'))
    MusicName = db.Column(db.String(100), nullable=False)
    Intro = db.Column(db.String(200))
    price = db.Column(db.DECIMAL(10,2), nullable=False, default=0.00)
    StorageLocation = db.Column(db.String(300), nullable=False)
    IssueTime = db.Column(db.DateTime, nullable=False)
    Cover = db.Column(db.String(300))

class SingerModel(db.Model):
    __tablename__ = '歌手'

    SingerID = db.Column(db.Integer, primary_key=True)
    Singer = db.Column(db.String(30), nullable=False)
    SingerSex = db.Column(db.Enum("男", "女"))

class SingingModel(db.Model):
    __tablename__ = '演唱'

    SingerID = db.Column(db.Integer,  db.ForeignKey('歌手.SingerID'), primary_key=True)
    MusicID = db.Column(db.Integer, db.ForeignKey('音乐.MusicID'), primary_key=True)

class CommentModel(db.Model):
    __tablename__ = '评论'
    CommentID = db.Column(db.Integer, primary_key=True)
    Content = db.Column(db.String(200))
    CommentTime = db.Column(db.DateTime, nullable=False)
    MusicID = db.Column(db.Integer, db.ForeignKey('音乐.MusicID'))
    UserID = db.Column(db.String(11), db.ForeignKey('用户.UserID'))

class ChartModel(db.Model):
    __tablename__ = '榜单'
    ChartID = db.Column(db.Integer, primary_key=True)
    ChartType = db.Column(db.String(25), nullable=False)

class CRankModel(db.Model):
    __tablename__ = '登榜'
    MusicID = db.Column(db.Integer, db.ForeignKey('音乐.MusicID'), primary_key=True)
    ChartID = db.Column(db.Integer, db.ForeignKey('音乐.MusicID'), primary_key=True)
    SongRanking = db.Column(db.Integer, nullable=False)

class OrderModel(db.Model):
    __tablename__ = '订单'

    OrderID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.String(11), db.ForeignKey('用户.UserID'))
    OrderTime = db.Column(db.DateTime, nullable=False)
    DownloadStatus = db.Column(db.Enum("0", "1"))

class OrderingModel(db.Model):
    __tablename__ = '下单'
    OrderID = db.Column(db.Integer, db.ForeignKey('订单.OrderID'), primary_key=True)
    MusicID = db.Column(db.Integer, db.ForeignKey('音乐.MusicID'), primary_key=True)

class AdvertisingID(db.Model):
    __tablename__ = '广告'
    AdvertisingID = db.Column(db.Integer, primary_key=True)
    Abstract = db.Column(db.String(100))
    title = db.Column(db.String(40))
    ReleaseTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    Picture = db.Column(db.String(200))

class Admin(db.Model):
    __tablename__ = '管理员'
    AdmID = db.Column(db.Integer, primary_key=True)
    AdmName = db.Column(db.String(50))
    Aassword = db.Column(db.String(20))

def get_songs(musicname):
    # 查询给定歌名的所有歌曲信息和对应的歌手信息
    song_singer = db.session.query(MusicModel, SingerModel).\
        join(SingingModel, MusicModel.MusicID == SingingModel.MusicID).\
        join(SingerModel, SingerModel.SingerID == SingingModel.SingerID).\
        filter(MusicModel.MusicName.contains(musicname)).all()
    # 使用 join 连接这三个表，连接条件是 MusicModel 的 MusicID 等于 SingingModel 的 MusicID
    #               以及 SingerModel 的 SingerID 等于 SingingModel 的 SingerID
    # filter 条件是 MusicModel 的 MusicName 等于 '给定歌名'
    # all() 方法返回所有符合条件的记录
    # song_singer是一个包含多个元组的列表。每个元组对应一个符合查询条件的记录
    # 其中第一个元素是MusicModel实例对象，第二个元素是SingerModel实例对象。
    return song_singer

def get_songs_(singername):
    # 查询给定歌首的所有歌曲信息
    singer_song = db.session.query(MusicModel, SingerModel).\
        join(SingingModel, MusicModel.MusicID == SingingModel.MusicID).\
        join(SingerModel, SingerModel.SingerID == SingingModel.SingerID).\
        filter(SingerModel.Singer.contains(singername)).all()
    # 使用 join 连接这三个表，连接条件是 MusicModel 的 MusicID 等于 SingingModel 的 MusicID
    #               以及 SingerModel 的 SingerID 等于 SingingModel 的 SingerID
    # filter 条件是 SingerModel.Singer 等于 '给定歌首'
    # all() 方法返回所有符合条件的记录
    # singer_song是一个包含多个元组的列表。每个元组对应一个符合查询条件的记录
    # 其中第一个元素是MusicModel实例对象，第二个元素是SingerModel实例对象。
    return singer_song

