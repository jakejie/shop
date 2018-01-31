# coding:utf-8
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
import multiprocessing,time
# 引入数据库数据表模型
from flask_migrate import upgrade
from app.model import User, Orders, Detail, Goods, BuyCar, Collect, \
    Comment, Address, TagList, Tags, Tag, Count, UserLog

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
# Global variables to jiajia2 environment:==设置为全局变量 在HTML里可以直接使用以下参数
app.jinja_env.globals['Count'] = Count


# app.jinja_env.globals['User'] = User
# app.jinja_env.globals['Orders'] = Orders
# app.jinja_env.globals['Goods'] = Goods
# app.jinja_env.globals['Address'] = Address
# app.jinja_env.globals['TagList'] = TagList
# app.jinja_env.globals['Tag'] = Tag
# app.jinja_env.globals['Tags'] = Tags


def make_shell_context():
    return dict(db=db, User=User,
                Orders=Orders, Goods=Goods,
                Address=Address, TagList=TagList,
                Tag=Tag, Tags=Tags,
                Collect=Collect, Comment=Comment, BuyCar=BuyCar,
                Detail=Detail, UserLog=UserLog
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


def worker_1(ids):
    manager.run()


def worker_2(ids):
    while True:
        print("hello {}".format(time.time()))
        time.sleep(3)


if __name__ == '__main__':
    # 开启多线程
    manager.run()
    """
    线程1：正常运行程序
    线程2：运行统计数据
    线程3：还没想好
    """
    # p1 = multiprocessing.Process(target=worker_1, args=(2,))
    # p2 = multiprocessing.Process(target=worker_2, args=(3,))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()

