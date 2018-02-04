from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from df_goods.models import GoodsInfo
from .models import *
from hashlib import sha1
from . import users_decorator

# Create your views here.


def register(request):
    return render(request, 'df_user/register.html')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    # print(type(count))
    # print('--------------')
    # ajax的请求需要返回一个json字符串，所以用JsonResponse返回，并且需要手动构造一个{'': }结构
    return JsonResponse({'count': count})


def register_handle(request):
    # 接受用户请求
    post = request.POST
    uname = post['user_name'].encode()
    upwd = post['pwd']
    upwd2 = post['cpwd']
    uemail = post['email']
    # 确认密码与原密码不一致
    if upwd != upwd2:
        return redirect('/user/register')
    # 密码加密
    # print(type(upwd))
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd3 = s1.hexdigest()

    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail

    # 保存用户,即提交到数据库
    user.save()
    # 重定向到登陆界面
    return redirect('/user/login/')


def login(request):
    # 在登陆成功时才会设置uname这个cookie,所以可以获取，如果没有则返回 ""
    uname = request.COOKIES.get('uname', '')

    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 接受用户名及密码
    post = request.POST
    uname = post['username']
    print(uname)
    upwd = post['pwd']
    # 如果接受到jizhu有值。就不用下面的默认值0
    jizhu = post.get('jizhu', 0)
    print(type(jizhu))
    # 通过models类中实体类.objects.filter 来查询数据库信息
    # 查询时，如果用get的方式，查不到就会报错。用filter则不会
    f_user = UserInfo.objects.filter(uname=uname)
    # 根据用户名到数据库获取对应信息
    print(f_user)
    if len(f_user) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        # 此处证明密码对上了
        if s1.hexdigest() == f_user[0].upwd:
            # HttpResponseRedirect继承于 HttpResponse
            red = HttpResponseRedirect('/user/info/')
            if jizhu != 0:
                # 如果jizhu!=0,这需要记住用户名。所以通过设置cookie的方式获取值
                red.set_cookie('uname', uname)
                #
            else:
                # 设置-1表示只要请求执行到了这一步立马过期
                red.set_cookie('uname', '', max_age=-1)

                # 到达此处即登陆成功。
                # 登陆成功后，为了前端登陆状态的辨别，以及为了能使前端携带一定关于当前登录用户的信息
                # 所以可以将用户id 之类的主要信息存入session
            request.session['user_id'] = f_user[0].id
            request.session['user_name'] = uname
            url = request.COOKIES.get('url', '')
            if len(url) != 0:
                return redirect(url)
                # print('-'*100)
            else:
                # print('+'*100)
                return red
        else:
            # 0 代表错了 1 代表对了
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        # context{}中，之所以要返回页面传过来的信息，是为了可以将错误信息返回给用户，以便用户在这个基础上继续修改
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


@users_decorator.login
# info = login(info)
def info(reqeust):
    user_id = reqeust.session['user_id']
    user_email = UserInfo.objects.get(id=reqeust.session['user_id']).uemail
    # UserInfo.objects.get获取的是这个类对象  UserInfo object
    # UserInfo.objects.fliter获取的是符合过滤条件的一个集合组 [<UserInfo: UserInfo object>]
    # print(UserInfo.objects.filter(id=reqeust.session['user_id']))
    goods_list = []
    goods_ids = reqeust.COOKIES.get('goods_ids', '')
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')  # ['']
        # GoodsInfo.objects.filter(id__in=goods_ids1)
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context = {'title': '用户中心-个人信息',
               'user_email': user_email,
               'user_name': reqeust.session['user_name'],
               'goods_list': goods_list
               }
    return render(reqeust, 'df_user/user_center_info.html', context)


@users_decorator.login
def order(reqeust):
    context = {'title': '用户中心-订单列表'}
    return render(reqeust, 'df_user/user_center_order.html',context)


@users_decorator.login
def site(reqeust):
    user = UserInfo.objects.get(id=reqeust.session['user_id'])

    # 这一个判断就能分隔post和get请求，如果是登陆成功
    # 转发过来的就是get请求，不经过下面判断题，
    # 否则即是表单提交所得值
    if reqeust.method == 'POST':
        user.ushou = reqeust.POST['ushou']
        user.uaddress = reqeust.POST['uaddress']
        user.uyoubian = reqeust.POST['uyoubian']
        user.uphone = reqeust.POST['uphone']
        user.save()
    context = {'title': '用户中心-收货地址', 'user': user}
    return render(reqeust, 'df_user/user_center_site.html', context)


