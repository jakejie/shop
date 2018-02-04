from django.http import HttpResponseRedirect


def login(func):
    def login_fun(request, *args, **kwargs):
        # print('='*100)
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login')
            red.set_cookie('url', request.get_full_path())
            return red
    return login_fun

# decorator
# def x(y):
#     def z():
#         y()
#     return z
#
#
# def a(b):
#     def c():
#         b()
#     return c
#