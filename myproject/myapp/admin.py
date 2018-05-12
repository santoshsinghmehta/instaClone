# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db import models
# Register your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    has_verified_mobile = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
