# encoding:utf8
# from . import mail
from flask_mail import Message
from flask import render_template, current_app


# def send_email(to, subject, template, **kwargs):
#     app = current_app._get_current_object()  # 这里不太懂，牵扯到异步，反正是配置验证信息的
#     msg = Message(subject, sender='418836702@qq.com', recipients=[to])  # 实例化一个Message对象，准备发送邮件，接受者为to
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html',
#                                **kwargs)  # 将准备好的模板添加到msg对象上，字典传的参里包括token(即生成的一长串字符串)，链接的组装，页面的渲染在里面用jinja2语法完成
#     with app.app_context():
#         mail.send(msg)  # 发射


# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from os import path
import os


class SendEmail(object):
    # 发送邮箱设置
    from_addr = "jakejie@163.com"
    password = "zhujie165102"
    smtp_server = 'smtp.163.com'

    def __init__(self, text, sender, receiver, subject, address):
        self.text = text
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.address = address
        self.to_addr = address
        # 从上到下依次是: 邮件内容,邮件发送者昵称,邮件接收者昵称,邮件主题
        self.msg = MIMEText(self.text, 'plain', 'utf-8')
        self.msg['From'] = self._format_addr(self.sender + '<' + self.from_addr + '>')
        self.msg['To'] = self._format_addr(self.receiver + '<' + self.to_addr + '>')
        self.msg['Subject'] = Header(self.subject, 'utf-8').encode()

    # 编写了一个函数_format_addr()来格式化一个邮件地址
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send(self):
        # server = smtplib.SMTP(self.smtp_server, 25)  # 25是普通接口，465 SSL接口
        server = smtplib.SMTP_SSL(self.smtp_server, 465)
        # server.starttls()  # SSL要求这句
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [self.to_addr], self.msg.as_string())
        server.quit()

# if __name__ == '__main__':
    # sendemail = SendEmail('111', 'wo', 'ni', 'zhuti', 'yangzd1993@foxmail.com')
    # sendemail.send()
