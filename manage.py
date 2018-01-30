# coding:utf-8
from flask import render_template, make_response, request
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

# 引入数据库数据表模型
from flask_migrate import upgrade
from app.model import User, Orders, Goods, Address, \
    TagList, Tag

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


def make_shell_context():
    return dict(db=db, User=User,
                Orders=Orders, Goods=Goods,
                Address=Address, TagList=TagList,
                Tag=Tag,
                )


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def deploy():
    # 创建所需数据表
    db.create_all()
    upgrade()


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
