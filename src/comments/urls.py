from django.contrib import admin
from django.urls import path
from comments import views

app_name = 'comments'

urlpatterns = [
    path('<int:id>',views.comment_thread,name='thread'),
    path('<int:id>/delete',views.comment_delete,name='delete'),

]
