# from django.shortcuts import render
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from backend.helpers import InputErrorMessage, JSONResponse
from .models import UserSerialiser, User


# Create your views here.
class UserShow(APIView):
    def get(self, request, format=None):
        serializer = UserSerialiser(request.user)
        return JSONResponse(serializer.data)

class Register(APIView):
    permission_classes = (AllowAny, )
    
    def post(self, request):

        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return InputErrorMessage("Invalid JSON body")
        if "username" not in data:
            return InputErrorMessage("username not provide.")
        if User.objects.filter(username=data["username"]).exists():
            return InputErrorMessage("username is used.")
        if "email" not in data:
            return InputErrorMessage("email not provide.")
        if User.objects.filter(email=data["email"]).exists():
            return InputErrorMessage("email is used.")
        if "password" not in data:
            return InputErrorMessage("password not provide.")
        user = User.objects.create_user(username=data["username"], email=data["email"], password=data["password"])
        user.save()
        return JSONResponse({
            "code": 200,
            "message": "OK",
        })