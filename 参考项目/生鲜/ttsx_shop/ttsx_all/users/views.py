from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from order.models import *
from .functions import *
from utils.wrappers import *
from .tasks import register_success


# 注册
def register(request):
    infos = get_messages(request)
    print(infos)
    return render(request, 'users/register.html', locals())


# 注册处理
def register_handle(request):
    # 检查参数
    # 验证通过
    if check_register_param(request):
        # 1.数据入库
        User.objects.user_register_save(request)
        # 发送注册成功邮件
        register_success()
        # 2.返回登陆界面
        return redirect(reverse("users:login"))
    # 验证失败
    else:
        # 返回注册页面
        return redirect(reverse("users:register"))


# 注册时检测用户名
def register_check_username(request):
    if username_exists(request):
        return JsonResponse({'ret': 1})
    else:
        return JsonResponse({'ret': 0})


# 登陆
def login(request):
    return render(request, 'users/login.html', locals())


# 检查登录参数
def login_handle(request):
    # 参数符合要求
    if check_login_params(request):
        # 1.记住用户信息
        # 获取跳转页面
        url = get_redirect_url(request)
        response = redirect(url)
        # 保存cookie
        reme_username(request, response)
        # 2.保存session
        keep_status_online(request)
        return response
    else:
        return redirect(reverse('users:register'))


# 注销登录
def logout(request):
    # 获取跳转页面
    url = get_redirect_url(request)
    # 删除session
    del_session(request)
    # 删除页面缓存
    from django.core.cache import cache
    cache.set('index', None, 0)
    cache.set('goods_list', None, 0)
    cache.set('detail', None, 0)
    # 默认跳转首页
    return redirect(url)


@check_user_login
# 用户中心信息
def user_center_info(request):
    user = User.objects.user_by_username(get_session(request, 'user_name'))
    # 查询出用户浏览记录表
    return render(request, 'users/user_center_info.html', locals())


@check_user_login
# 用户中心地址
def user_center_site(request):
    user = User.objects.user_by_username(get_session(request, 'user_name'))
    return render(request, 'users/user_center_site.html', locals())


@check_user_login
# 编辑地址
def user_center_site_edit(request):
    if check_site_params(request):
        # 地址数据入库
        User.objects.user_site_save(request)
    return redirect(reverse('users:user_center_site'))


@check_user_login
# 用户中心订单
def user_center_order(request):
    # 获取当前用户所有订单
    orders = Order.objects.filter(order_user_id=get_session(request, 'uid'))
    # 创建分页对象
    paginator = Paginator(orders, 2)
    # 获得当前页码
    current_page = get(request, 'page')
    if not current_page:
        current_page = 1
    orders = paginator.page(current_page)
    for order in orders:
        order.total = 0
        for goods in order.goodsdetail_set.all():
            order.single = goods.goods_price * goods.goods_num
            order.total += order.single
    return render(request, 'users/user_center_order.html', locals())
