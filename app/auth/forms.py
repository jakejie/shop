from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.model import User


# 注册表单
class RegistForm(FlaskForm):
    username = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称")

        ],
        description="昵称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称！",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱"),
            Email('邮箱格式不正确')

        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱！",

        }
    )
    phone = StringField(
        label="手机号码",
        validators=[
            DataRequired("请输入手机号码"),
            Regexp('1[3578]\\d{9}', message='手机格式不正确')

        ],
        description="手机号码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码！",

        }
    )
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码！",

        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码"),
            EqualTo('password', message='两次输入的密码不一致')
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入确认密码！",

        }
    )
    submit = SubmitField(
        '注册',
        render_kw={"class": "btn btn-lg btn-success btn-block", }
    )

    def validate_name(self, field):
        username = field.data
        user = User.query.filter_by(name=username).count()
        if user == 1:
            raise ValidationError("昵称已经存在")

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已经存在")

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("手机已经存在")


# 登录表单
class LoginForm(FlaskForm):
    username = StringField(
        label='账号',
        validators=[
            DataRequired("请输入账号"),
            # Regexp('1[3578]\\d{9}', message='手机格式不正确')

        ],
        description="账号",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入用户名！",
        }
    )
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码！",

        }
    )
    submit = SubmitField(
        '登录',
        render_kw={"class": "btn btn-lg btn-primary btn-block", }
    )
