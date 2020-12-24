"""trydjango19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('create',views.post_create,name='postcreate'),
    path('<int:id>',views.post_details,name='postdetails'),
    path('<int:id>/edit',views.post_update,name='postupdate'),
    path('list',views.post_list,name='postlist'),
    path('<int:id>/delete',views.post_delete,name='postdelete'),
]
