from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from rest_framework import serializers
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')