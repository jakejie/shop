# coding: utf-8
import time
from celery import task
from django.core.mail import send_mail
from django.conf import settings


@task
def register_success():
    content = '注册成功！'
    send_mail(subject='注册邮件',
              message=content,
              from_email=settings.EMAIL_FROM,
              recipient_list=settings.EMAIL_TO_LIST,
              html_message='', )

