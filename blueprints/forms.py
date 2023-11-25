import wtforms
from flask import g
from wtforms.validators import Email, Length, EqualTo, AnyOf
from models import UserModel, EmailCaptchaModel
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
        if user:  # 不为空
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
