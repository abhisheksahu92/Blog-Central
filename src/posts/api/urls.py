from django.contrib import admin
from django.urls import path
from .views import PostCreateApiView,PostDeleteApiView,PostUpdateApiView,PostDetailApiView,PostListApiView

app_name = 'posts'

urlpatterns = [
    path('',PostListApiView.as_view(),name='postapilist'),
    path('create',PostCreateApiView.as_view(),name='postapicreate'),
    path('<slug:slug>',PostDetailApiView.as_view(),name='postapidetails'),
    path('<slug:slug>/edit',PostUpdateApiView.as_view(),name='postapiupdate'),
    path('<slug:slug>/delete',PostDeleteApiView.as_view(),name='postapidelete'),

]