from flask_login import login_required, current_user, logout_user, login_user
from flask import redirect, url_for, render_template, request, flash, session
from . import auth
from .forms import RegistForm, LoginForm, ChangePassWord
from werkzeug.security import generate_password_hash
import uuid
from app.model import User, UserLog
from app import db


# 在请求之前验证该账号是否经过邮箱验证  待开发
# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated \
#             and not current_user.confirmed \
#             and request.endpoint[:5] != 'auth.' \
#             and request.endpoint != 'static':
#         return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        # 如果你已经激活过了 跳转到主页
        return redirect(url_for('home.index'))
    if current_user.confirm(token):
        # 去激活并且激活成功了
        flash('O了！')
    else:
        flash('你是盗号的还是迟到鬼?')
    return redirect(url_for('main.index'))


# 登录页=ok
@auth.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            flash('用户名不存在', 'err')
            return redirect(url_for('auth.login'))
        if not user.check_pwd(data['password']):
            flash('密码错误', 'err')
            return redirect(url_for('auth.login'))
        session['user'] = user.username
        session['user_id'] = user.id
        # 记录用户的登录状态
        login_user(user, True)
        """
        login_user函数的第一个参数是需要登录的用户对象，
        第二个参数是bool值，如果为False，
        那么关闭浏览器后用户会话就会中断，
        下次用户访问时需要重新登录。
        如果为True，那么会在浏览器中写入一个长期有效的cookie，
        使用该cookie可以复原用户会话。
        """
        userlog = UserLog(
            user_logs=user.id,
            ip_add=request.remote_addr,
            remark="登陆",
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.user'))
    return render_template("auth/login.html", form=form)


# 注册页=ok
@auth.route('/register/', methods=["POST", "GET"])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            pwd=data['password'],
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功', 'ok')
        # 注册成功后 跳转到登陆页面
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


# 退出登陆=ok
@auth.route('/logout')
@login_required
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    logout_user()
    return redirect(url_for("auth.login"))


# 修改密码页面
@auth.route('/pwd', methods=["POST", "GET"])
@login_required
def change_pwd():
    form = ChangePassWord()
    if form.validate_on_submit():
        if current_user.check_pwd(form.old_password.data):
            # 这里引入user的上下文，这个概念不太懂，暂且当成全局变量来用
            current_user.password = form.password.data
            current_user.password = generate_password_hash(form.password.data)
            current_user.pwd = form.password.data
            # 修改密码
            db.session.add(current_user)
            db.session.commit()
            # 记录到日志
            userlog = UserLog(
                user_logs=current_user.id,
                ip_add=request.remote_addr,
                remark="修改密码",
            )
            db.session.add(userlog)
            db.session.commit()
            # 加入数据库的session，这里不需要.commit()，在配置文件中已经配置了自动保存
            flash('密码修改成功！', "ok")
            # 跳转到个人中心
            return redirect(url_for('home.user'))
        else:
            flash('密码修改失败！')
            return redirect(url_for('home.user'))
    return render_template('auth/change_pwd.html', form=form)


# 忘记密码
@auth.route('/forget_password/')
def forget_password():
    return render_template('auth/forgetpwd.html')
