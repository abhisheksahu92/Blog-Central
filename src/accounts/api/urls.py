from django.contrib import admin
from django.urls import path
from .views import UserCreateApiView,UserLoginApiView

app_name = 'usersapi'

urlpatterns = [
    path('register',UserCreateApiView.as_view(),name='usercreateapi'),
    path('login',UserLoginApiView.as_view(),name='userloginapi'),

]
