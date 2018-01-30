# coding:utf-8
from flask import render_template, make_response, request
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

# 引入数据库数据表模型
from flask_migrate import upgrade
# from app.models import CinemaDetail, CityData, \
#     ShowData, MovieInfo, PageView, User,CinemaData


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
#
# # Global variables to jiajia2 environment:
# app.jinja_env.globals['CinemaDetail'] = CinemaDetail
# app.jinja_env.globals['CityList'] = CityData
# app.jinja_env.globals['HotCinemaData'] = HotCinemaData
# app.jinja_env.globals['HotMovie'] = HotMovie
# app.jinja_env.globals['ShowData'] = ShowData
# app.jinja_env.globals['MovieInfo'] = MovieInfo
# app.jinja_env.globals['WaitMovie'] = WaitMovie
# app.jinja_env.globals['PageView'] = PageView


#
#
# def make_shell_context():
#     return dict(db=db, User=User,
#                 CinemaDetail=CinemaDetail, CityList=CityData,
#                 # HotCinemaData=HotCinemaData, HotMovie=HotMovie,
#                 ShowData=ShowData, MovieInfo=MovieInfo,
#                 # WaitMovie=WaitMovie,
#                 PageView=PageView,
#                 )


# manager.add_command("shell", Shell(make_context=make_shell_context))


#
#
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
    manager.run()
