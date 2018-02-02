from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, FloatField, \
    SelectField, BooleanField
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms.validators import DataRequired


# 上传商品表单
class AddGoodsForm(FlaskForm):
    # 商品主页图片
    image = FileField(
        label="商品图片",
        validators=[
            DataRequired("请上传图片"),
            FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'bmp'], "只能上传图片！"),
            FileRequired("文件未选择！"),
        ],
        description="图片",
    )
    # 商品标题
    name = StringField(
        label="标题",
        validators=[
            DataRequired("请输入商品标题")
        ],
    )
    # 商品分类
    good_tag = SelectField(
        label="分类",
        validators=[DataRequired()],
        choices=[('0', '全部'), ('1', '待审核'), ('2', '认证成功'), ('3', '认证失败')]
    )
    # 章节数量
    chap_num = IntegerField(
        label="章节",
        validators=[
            DataRequired("请输入课程章节")
        ],
    )
    # 折扣
    discount = FloatField(
        label="折扣",
        validators=[
            DataRequired("请输入课程折扣")
        ],
        render_kw={
            "class": "form-control",
            "rows": 10,
            "id": "discount",
        }
    )
    # 商品原价
    old_price = FloatField(
        label="商品原价",
        validators=[
            DataRequired("请输入课程原价")
        ],
        render_kw={
            "class": "form-control",
            "rows": 10,
            "id": "old_price",
        }
    )
    # 商品现价
    price = FloatField(
        label="实际售价 请勿修改",
        validators=[
        ],
        render_kw={
            "class": "form-control",
            "rows": 10,
            "id": "price",
        }
    )
    # 星级
    start = SelectField(
        label="星级",
        choices=[('1', '一星'), ('2', '二星'), ('3', '三星'), ('4', '四星'), ('5', '五星')],
        validators=[
            DataRequired()
        ],
    )
    # 简介
    info = TextAreaField(
        label='简介',
        # validators=[
        #     DataRequired("请输入简介")
        # ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10,
            "style": "width:100%;height:500px",
        }
    )
    # 是否上架
    target = BooleanField(
        label="是否上架",
    )
    # 库存数
    skull_num = IntegerField(
        label="库存",
        validators=[
            DataRequired("请输入库存")
        ],
        description="库存",
        render_kw={
            "class": "form-control",
            "rows": 10,
        }
    )
    # 分享链接
    share_link = IntegerField(
        label="提取链接",
        validators=[
            DataRequired("请填写提取链接")
        ],
        description="链接",
        render_kw={
            "class": "form-control",
            "rows": 10,
        }
    )
    # 提取密码
    get_secure = IntegerField(
        label="提取密码",
        validators=[
            DataRequired("请填写提取密码")
        ],
        description="提取密码",
        render_kw={
            "class": "form-control",
            "rows": 10,
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={"class": "btn btn-success  ", }
    )
