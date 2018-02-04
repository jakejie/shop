#coding=utf-8
import hashlib 
from datetime import datetime

# 将手机号中间四位设置为*
def formatPhoneNumber(phone):
    return phone[0:3] + '*'*4 + phone[7:11]

# 将密码进行md5加密
def to_md5(string):
    result = hashlib.md5(string).hexdigest()
    return result

# 将时间转字符串 为 年-月-日 时：分：秒
def formateTime(orderTime):
    return orderTime.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    print(to_md5('123456'))
    # print(to_md5('avcaweq'))
    # print(formateTime(datetime(2016, 11, 1, 23, 5, 26, 375013)))