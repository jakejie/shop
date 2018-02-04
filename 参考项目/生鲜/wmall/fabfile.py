#!/usr/bin/env python
# coding:utf-8
# 线上数据库备份到本地

import sys,os,time
from fabric.api import local,cd,run,env,hosts

# def hello(name):
#     #print ('hellp fab!')
#     print 'hello %s !' % name
# env.hosts = ['192.168.3.200']
env.hosts = ['localhost']
env.password = 'root'

# def test():
#     local('cd /home/')
#     local('ls -l|wc -l')

# def test():
#     with cd('/home'):
#         run('du -sh')


# def setting_ci():
#     local('echo "add and commit settings in local"')
#
# def update_setting_remote():
#     print "remote update"
#     with cd('/home'):
#         run('ls -l | wc -l')

print ('start backup database .....')
# dbnameList = ['dodoca','python']
dbnameList = {
    #  '192.168.3.200': {
    #     'dbhost': '192.168.3.200',
    #     'dbuser': 'root',
    #     'dbpass': 'dodoca',
    #     'dbname': 'weixin2014',
    #     'charset': 'utf8',
    #     'serviceIp': '192.168.3.200',
    #     'username': 'root'
    # },
    'localhost': {
        'dbhost': 'localhost',
        'dbuser': 'root',
        'dbpass': '123456',
        'dbname': 'python',
        'charset': 'utf8',
        'serviceIp': '192.168.3.200',
        'username': 'root'
    },
}
db_backup = '/mnt/hgfs/www/python/wmall/db_backup'
logs_path = '/mnt/hgfs/www/python/wmall/db_backup'
c_date = time.strftime('%Y-%m-%d')
c_time = time.strftime('%y%m%d%H%M%S')
# dbhost = 'localhost'
# dbuser = 'root'
# dbpass = '123456'
# dbhost = 'localhost'
#
# username = 'root'
# serviceIp = '192.168.3.200'


# 日志
def wLogs(filename,contents):
    f = open(filename,'a+')
    f.write(contents + '\n')
    f.close()

# 备份文件
def mysqlBackup():
    log_file = logs_path + '/' + c_date + '.txt'
    if dbnameList:
        for dbname in dbnameList:
            # print dbname
            print dbnameList[dbname]['dbhost']
            db_backup_name = db_backup + '/' + dbnameList[dbname]['dbname'] + '_' + c_date + '.sql'
            db_backup_cmd = 'mysqldump -h%s -u%s -p%s %s > %s ' % (dbnameList[dbname]['dbhost'],dbnameList[dbname]['dbuser'],dbnameList[dbname]['dbpass'],dbnameList[dbname]['dbname'],db_backup_name)
            run(db_backup_cmd)
            target_file = '/root/cdh'
            scpToService(db_backup_name, target_file,dbnameList[dbname]['username'],dbnameList[dbname]['serviceIp'])
            content = c_time + ' : ' + 'db:' + dbnameList[dbname]['dbhost'] + ' , backup sucsess !'
            wLogs(log_file,content)

# 复制文件到服务器
def scpToService(source_file, target_file,username,host):
    if source_file and target_file:
        cp_cmd = 'scp ' + source_file + ' ' + username + '@' + host + ':' + target_file
        print 'scp starting ....'
        run(cp_cmd)
        print 'end'
    else:
        print 'must be filepath'


'''
 复制文件到本地
 文件名使用绝对路径
'''
def scpToLocal(source_file, target_file,username,host):
    if source_file and target_file:
        cp_cmd = 'scp ' + username + '@' + host + ':' + source_file + ' ' + target_file
        print 'scp starting ....'
        run(cp_cmd)
        print 'end'
    else:
        print 'must be filepath'

print ('end .....')
# def update():
#     setting_ci()
#     update_setting_remote()


    