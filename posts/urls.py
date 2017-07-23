from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^create/',views.post_create,name='create'),
]