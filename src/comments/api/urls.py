from django.contrib import admin
from django.urls import path
from .views import CommentListApiView,CommentDetailApiView,CommentCreateApiView

app_name = 'commentsapi'

urlpatterns = [
    path('',CommentListApiView.as_view(),name='commentlistapi'),
    path('create',CommentCreateApiView.as_view(),name='commentcreateapi'),
    path('<int:pk>',CommentDetailApiView.as_view(),name='commentdetailapi'),
]
