from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField,FloatField ,\
    SelectField, BooleanField

from flask_wtf.file import FileAllowed, FileRequired, FileField, DataRequired

from wtforms.validators import DataRequired
from wtforms.validators import Required


class AddGoodsForm(FlaskForm):
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
    # 折扣价
    price = FloatField(
        label="折扣价",
        validators=[
            DataRequired("请输入课程价格")
        ],
    )
    # 商品原价
    old_price = FloatField(
        label="商品原价",
        validators=[
            DataRequired("请输入课程原价")
        ],
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

        }
    )
    # 是否上架
    target = BooleanField(
        label="是否上架",
    )
    submit = SubmitField(
        '提交',
        render_kw={"class": "btn btn-success  ", }
    )
