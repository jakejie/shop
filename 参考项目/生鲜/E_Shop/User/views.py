from django.shortcuts import render
from view.views import *
from utils.userutils import *
from django import forms
# Create your views here.


# 数据验证
class UserForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField()
    type = forms.CharField()

    def clean(self):
        super(UserForm, self).clean()
        try:
            username = self.cleaned_data['username']

            email_server_suggest = ['qq', 'gmail', '163', '126', 'sina']
            if username[username.index('@')+1: username.index('.')] not in email_server_suggest:
                self.errors['username'] = ['不支持此邮箱服务']
        except Exception:
            pass


class RegisterView(BaseView):
    template_name = 'register.html'

    def get_extra_context(self, request, *args, **kwargs):
        context = {}

        # 获取可能产生的异常
        errorType = 'registerError'
        isRedirct = request.session.get('redirct', '')

        if isRedirct != 'True':
            request.session['errorType'] = ''
            request.session['loginError'] = ''
            request.session['registerError'] = ''

        error_message = request.session.get(errorType, '')
        request.session['redirct'] = 'False'
        context = {
            'error': error_message
        }

        return context


class RegisterControlView(BaseRedirctView, UserCenter):
    form_cls = UserForm

    # 清空遗留出错信息
    def error_initialize(self):
        self.request.session['errorType'] = ''
        self.request.session['loginError'] = ''
        self.request.session['registerError'] = ''
        self.request.session['redirct'] = 'False'

    def handle(self, request, *args, **kwargs):

        # 数据清洗
        form = self.form_cls(request.POST.dict())
        if form.is_valid():
            if hasattr(self, 'user_dispath'):
                self.error_initialize()
                user = getattr(self, 'user_dispath')(request, **form.cleaned_data)

                if user is None:
                    self.request.session['redirct'] = 'True'
                    self.redirct_url = '/user/register/'
                else:
                    self.redirct_url = '/user/usercenter/'

            else:
                return HttpResponseBadRequest('没有实现user_dispath方法')
        else:
            """
            数据清洗过程中，出现违法数据通过json返回错误信息。在前端使用js处理。
            """
            self.redirct_url = '/user/register/'
            return JsonResponse({'errorcode': -300, 'errormsg': form.errors})


class LoginView(BaseView):
    template_name = 'login.html'

    def get_extra_context(self, request, *args, **kwargs):
        context = {}

        # 获取可能产生的异常
        errorType = 'loginError'
        isRedirct = request.session.get('redirct', '')

        if isRedirct != 'True':
            request.session['errorType'] = ''
            request.session['loginError'] = ''
            request.session['registerError'] = ''

        error_message = request.session.get(errorType, '')
        request.session['redirct'] = 'False'
        context = {
            'error': error_message
        }

        return context


class LoginControl(BaseRedirctView, UserCenter):

    # 清空遗留出错信息
    def error_initialize(self):
        self.request.session['errorType'] = ''
        self.request.session['loginError'] = ''
        self.request.session['registerError'] = ''
        self.request.session['redirct'] = 'False'

    def handle(self, request, *args, **kwargs):
        if hasattr(self, 'user_dispath'):
            self.error_initialize()
            user = getattr(self, 'user_dispath')(request, *args, **kwargs)

            if user is None:
                self.request.session['redirct'] = 'True'
                self.redirct_url = '/user/login/'
            else:
                self.redirct_url = '/user/usercenter/'

        else:
            return HttpResponseBadRequest('没有实现user_dispath方法')


class UserCenterView(BaseView):
    template_name = 'user.html'


from utils.commonutils import *
from django import forms


class AddressForm(forms.Form):
    provinceid = forms.IntegerField(required=False)
    cityid = forms.IntegerField(required=False)
    areaid = forms.IntegerField(required=False)
    details = forms.CharField(required=False)
    name = forms.CharField(required=False)
    phone = forms.CharField(required=False)


class AddressView(BaseView,OperateView):
    form_cls = AddressForm
    template_name = 'address.html'

    def get_extra_context(self, request, *args, **kwargs):
        default_citys = get_citys_by_id(provinces[0]['id'])
        default_areas = get_ares_by_id(default_citys[0]['id'])
        user = request.session['user']
        user = User.objects.get(user = user['user'])
        address = user.address_set.all()
        return {'provinces': provinces, 'citys': default_citys, 'areas': default_areas, 'address':address}

    def get_province(self, request, provinceid, *args, **kwargs):
        citys = get_citys_by_id(str(provinceid))
        areas = get_ares_by_id(citys[0]['id'])
        return {'citys':citys, 'areas':areas}

    def get_citys(self, request, cityid, *args, **kwargs):
        areas = get_ares_by_id(str(cityid))
        return {'areas': areas}

    def save_address(self, request, name, phone, provinceid, areaid, cityid, details):
        user = request.session['user']
        user = User.objects.get(user=user['user'])
        province = get_province_by_id(provinceid)
        city = get_city_by_id(provinceid, cityid)
        area = get_area_by_id(cityid, areaid)
        try:
            address = Address.objects.create(name=name, phone=phone, province=province, city=city, area=area, details=details, user=user)
            return {'errorcode': 200, 'errormsg': ''}
        except:
            return {'errorcode': -300, 'errormsg': '添加失败'}


