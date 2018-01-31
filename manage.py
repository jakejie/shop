# coding:utf-8
from flask import render_template, make_response, request
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

# 引入数据库数据表模型
from flask_migrate import upgrade
from app.model import User, Orders, Goods, Address, \
    TagList, Tags, Tag

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
#
# # Global variables to jiajia2 environment:
app.jinja_env.globals['User'] = User
app.jinja_env.globals['Orders'] = Orders
app.jinja_env.globals['Goods'] = Goods
app.jinja_env.globals['Address'] = Address
app.jinja_env.globals['TagList'] = TagList
app.jinja_env.globals['Tag'] = Tag
app.jinja_env.globals['Tags'] = Tags


def make_shell_context():
    return dict(db=db, User=User,
                Orders=Orders, Goods=Goods,
                Address=Address, TagList=TagList,
                Tag=Tag, Tags=Tags,
                )


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def deploy():
    # 创建所需数据表
    db.create_all()
    upgrade()


@manager.command
def one():
    import requests
    from lxml import etree
    url = "https://chuanke.baidu.com/?mod=search&act=course&do=nav"
    response = requests.get(url)
    tree = etree.HTML(response.text)
    categ_m = tree.xpath('//div[@class="categ_m"]')
    for categ in categ_m:
        tag = "".join(categ.xpath('h3/a/text()'))
        i = TagList(
            name=tag,
        )
        try:
            db.session.add(i)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        dls = categ.xpath('dl')
        for dl in dls:
            namess = "".join(dl.xpath('dt/a/text()')).replace('\u3000\u3000', '').replace('\u3000', '')
            t = Tags(
                f_name=tag,
                name=namess,
            )
            try:
                db.session.add(t)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

            infos = dl.xpath('dd/a')
            for info in infos:
                dd = "".join(info.xpath('text()'))
                s = Tag(
                    t_name=namess,
                    name=dd,
                )
                try:
                    db.session.add(s)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)


@app.before_first_request
@app.route("/")
def index():
    return "哈哈哈哈或或或或"


if __name__ == '__main__':
    # 开启多线程
    """
    线程1：正常运行程序
    线程2：运行统计数据
    线程3：还没想好
    """
    manager.run()
