# -*- coding: utf-8 -*-
from django.db import models
from rest_framework import serializers

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    img = models.ImageField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'img')