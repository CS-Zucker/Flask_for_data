import wtforms
from flask import g
from wtforms.validators import Email, Length, EqualTo, AnyOf, NumberRange, DataRequired
from models import *
from exts import db
# 获取前端数据验证前端数据是否符合要求
class RegisterForm(wtforms.Form):  # 继承wtforms.Form
    UserID = wtforms.StringField(validators=[Length(min=11, max=11, message="账号格式错误")])
    Email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误")])
    UserName = wtforms.StringField(validators=[Length(min=2, max=30, message="用户名格式错误")])
    Password = wtforms.StringField(validators=[Length(min=6, max=20,  message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("Password", message="两次密码不一致")])  # 确认密码验证
    ContactNumber = wtforms.StringField(validators=[Length(min=11, max=11, message="手机号格式错误")])
    # 验证邮箱是否被注册
    def validate_Email(self, filed):  # filed指Email
        email = filed.data
        user = UserModel.query.filter_by(Email=email).first()   # 返回第一个与邮箱一样
        if user:  # 不为空
            raise wtforms.ValidationError(message="该邮箱已被注册")  # 抛出异常

        # 验证账号是否被注册
    def validate_UserID(self, filed):  # filed指Email
        userid = filed.data
        user = UserModel.query.get(userid)  # 返回第一个与邮箱一样
        if user:  # 不为空
            raise wtforms.ValidationError(message="该账号已被注册")  # 抛出异常

    # 验证码是否正确
    def validate_captcha(self, filed):  # filed指captcha
        captcha = filed.data
        email = self.Email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误")
        else:  # 验证通过就没有用了可以删掉
            db.session.delete(captcha_model)
            db.session.commit()

class LoginForm(wtforms.Form):
    Email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    Password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])


class AdminForm(wtforms.Form):
    AdminId = wtforms.StringField(validators=[Length(min=3, max=11, message="管理员ID格式错误")])
    Password = wtforms.StringField(validators=[Length(min=3, max=11, message="管理员密码格式错误")])


class PersonalForm(wtforms.Form):  # 继承wtforms.Form
    Email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    sex = wtforms.StringField(validators=[AnyOf(values=['男', '女'], message="性别格式错误")])
    UserName = wtforms.StringField(validators=[Length(min=2, max=30, message="用户名格式错误")])
    Password = wtforms.StringField(validators=[Length(min=6, max=20,  message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("Password", message="两次密码不一致")])  # 确认密码验证
    ContactNumber = wtforms.StringField(validators=[Length(min=11, max=11, message="手机号格式错误")])
    # 验证邮箱是否被注册
    def validate_Email(self, filed):  # filed指Email
        Email = filed.data
        user = UserModel.query.filter_by(Email=Email).first()   # 返回第一个与邮箱一样
        if user and user.Email != g.user.Email:  # 不为空
            raise wtforms.ValidationError(message="该邮箱已被注册")  # 抛出异常

    # 验证码是否正确
    def validate_captcha(self, filed):  # filed指captcha
        captcha = filed.data
        email = self.Email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误")
        else:  # 验证通过就没有用了可以删掉
            db.session.delete(captcha_model)
            db.session.commit()

# 添加用户验证
class AddUserForm(wtforms.Form):  # 继承wtforms.Form
    UserID = wtforms.StringField(validators=[Length(min=11, max=11, message="账号格式错误")])
    Email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    UserName = wtforms.StringField(validators=[Length(min=2, max=30, message="用户名格式错误")])
    Password = wtforms.StringField(validators=[Length(min=6, max=20,  message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("Password", message="两次密码不一致")])  # 确认密码验证
    ContactNumber = wtforms.StringField(validators=[Length(min=11, max=11, message="手机号格式错误")])
    # 验证邮箱是否被注册
    def validate_Email(self, filed):  # filed指Email
        Email = filed.data
        user = UserModel.query.filter_by(Email=Email).first()   # 返回第一个与邮箱一样
        if user:  # 不为空
            raise wtforms.ValidationError(message="该邮箱已被注册")  # 抛出异常
    def validate_UserID(self, filed):
        userid = filed.data
        user = UserModel.query.filter_by(UserID=userid).first()  # 返回第一个与邮箱一样
        if user:  # 不为空
            raise wtforms.ValidationError(message="该账号已被注册")  # 抛出异常

# 修改用户验证
class EditUserForm(wtforms.Form):  # 继承wtforms.Form
    Email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    UserName = wtforms.StringField(validators=[Length(min=2, max=30, message="用户名格式错误")])
    # 验证邮箱是否被注册
    def validate_Email(self, filed):  # filed指Email
        Email = filed.data
        user = UserModel.query.filter_by(Email=Email).first()   # 返回第一个与邮箱一样
        if user:
            raise wtforms.ValidationError(message="该邮箱已被注册")  # 抛出异常


class RepasswordForm(wtforms.Form):  # 继承wtforms.Form
    Email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误")])
    Password = wtforms.StringField(validators=[Length(min=6, max=20,  message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("Password", message="两次密码不一致")])  # 确认密码验证
    # 验证码是否正确
    def validate_captcha(self, filed):  # filed指captcha
        captcha = filed.data
        email = self.Email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误")
        else:  # 验证通过就没有用了可以删掉
            db.session.delete(captcha_model)
            db.session.commit()


# 添加音乐验证
class AddMusicForm(wtforms.Form):  # 继承wtforms.Form
    MusicID = wtforms.StringField(validators=[Length(min=5, max=5, message="音乐ID格式错误")])
    MusicName = wtforms.StringField(validators=[Length(min=1, max=30, message="音乐名格式错误")])
    Intro = wtforms.StringField(validators=[Length(min=0, max=200,  message="简介格式错误")])
    ClassID = wtforms.StringField(validators=[Length(min=3, max=3,  message="类型ID格式错误")])
    price = wtforms.DecimalField(validators=[NumberRange(min=0.00, max=999.99, message="价格格式错误")])  # 两位小数验证
    IssueTime = wtforms.DateTimeField(format="%Y-%m-%dT%H:%M")  # YYYY-MM-DD HH:MM:SS
    def validate_MusicID(self, filed):
        MusicID = filed.data
        music = MusicModel.query.filter_by(MusicID=MusicID).first()  # 返回第一个与邮箱一样
        if music:  # 不为空
            raise wtforms.ValidationError(message="该音乐ID已存在")  # 抛出异常
    def validate_ClassID(self, filed):
        ClassID = filed.data
        add_class = ClassModel.query.filter_by(ClassID=ClassID).first()  # 返回第一个与邮箱一样
        if add_class is None:  # 为空
            raise wtforms.ValidationError(message="该类别ID不存在")  # 抛出异常

# 修改音乐验证
class EditMusicForm(wtforms.Form):  # 继承wtforms.Form
    MusicName = wtforms.StringField(validators=[Length(min=1, max=30, message="音乐名格式错误")])
    Intro = wtforms.StringField(validators=[Length(min=0, max=200,  message="简介格式错误")])
    ClassID = wtforms.StringField(validators=[Length(min=3, max=3,  message="类型ID格式错误")])
    price = wtforms.DecimalField(validators=[NumberRange(min=0.00, max=999.99, message="价格格式错误")])  # 两位小数验证
    IssueTime = wtforms.DateTimeField(format="%Y-%m-%dT%H:%M")  # YYYY-MM-DD HH:MM:SS
    def validate_MusicID(self, filed):
        MusicID = filed.data
        music = MusicModel.query.filter_by(MusicID=MusicID).first()  # 返回第一个与邮箱一样
        if music:  # 不为空
            raise wtforms.ValidationError(message="该音乐ID已存在")  # 抛出异常
    def validate_ClassID(self, filed):
        ClassID = filed.data
        add_class = ClassModel.query.filter_by(ClassID=ClassID).first()  # 返回第一个与邮箱一样
        if add_class is None:  # 为空
            raise wtforms.ValidationError(message="该类别ID不存在")  # 抛出异常