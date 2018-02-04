from django.shortcuts import *
from django.shortcuts import redirect

def login(func):
	def wrapper(request,*args):
		userName = request.session.get('userName',default='')
		dic={
			'userName':userName
		}
		result = func(request,dic,*args)
		return result
	return wrapper

# def log_yz(func):
# 	def wrapper(request,*args):
# 		if request.session.has_key('userName'):
# 			result = func(request,*args)
# 		else:
# 			result= redirect('/login/')
# 		return result
# 	return wrapper

 