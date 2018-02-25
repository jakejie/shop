from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, IntegerField, HiddenField, \
    SelectField, StringField, BooleanField, DateField, PasswordField
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError
from app.model import User


# 修改会员信息表单
class UserDetailForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired("请输入昵称")
        ],
        description="昵称",
        render_kw={
            "class": "form-control",
            "rows": 10,

        }
    )
    birthday = DateField(
        label="生日",
        validators=[
            DataRequired("请输入生日")
        ],
    )
    sex = StringField(
        label="性别",
        validators=[
            DataRequired("请输入性别")
        ],
    )
    phone = StringField(
        label='电话',
        validators=[
            DataRequired("请输入电话"),
            Regexp('1[3578]\\d{9}', message='手机格式不正确')
        ],
        description="电话",
        render_kw={
            "class": "form-control",
            "rows": 10,
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired("请输入邮箱"),
            Email('邮箱格式不正确')
        ],
        description="邮箱",
        render_kw={
            "class": "form-control",
            "rows": 10,
        }
    )

    info = StringField(
        label='简介',
        validators=[
            DataRequired("请输入简介")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10,

        }
    )
    submit = SubmitField(
        '保存修改',
        render_kw={"class": "btn btn-success  ", }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(username=name).count()
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

    # 修改密码


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码！",
        }
    )
    submit = SubmitField(
        '修改密码',
        render_kw={
            "class": "btn btn-success",
        }
    )

    # image = FileField(
    #     label="头像",
    #     validators=[
    #         DataRequired("请上传头像"),
    #         FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'bmp'], "只能上传图片！"),
    #         FileRequired("文件未选择！"),
    #     ],
    #     description="头像",
    # )


# 添加评论记录
class CommentForm(FlaskForm):
    content = TextAreaField(
        label='评论',
        validators=[
            DataRequired("请输入评论信息")

        ],
        description="评论",
        render_kw={
            "class": "form-control",
            "rows": 10,
        }
    )
    comment_good_id = IntegerField(
        label='商品ID',
        description="",
        render_kw={
            "class": "form-control",
            "rows": 10,
        }
    )
    submit = SubmitField(
        '提交评论',
        render_kw={"class": "btn btn-success  ", }
    )


# 购物车选中商品去结算
class Buy(FlaskForm):
    pass


# 添加收货地址表单
class AddAddress(FlaskForm):
    # 省份
    province = SelectField()
    # 城市
    city = SelectField()
    # 地区
    area = SelectField()
    # 详细地址
    address = StringField()
    # 联系电话
    phone = StringField()
    # 姓名
    name = StringField()
    # 备注
    remarks = StringField()
    # 是否设置为默认地址
    default_add = BooleanField()
    # 提交数据
    submit = SubmitField(
        '提交',
        render_kw={"class": "btn btn-success  ", }
    )
