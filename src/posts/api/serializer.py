#restframework
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField,SerializerMethodField
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from python_http_client import client

#django modules
from posts.models import Post
from comments.models import Comment
from comments.api.serializer import CommentListSerializer
from accounts.api.serializer import UserDetailSerializer
from django.urls import reverse
from django.test import Client
from django.http import HttpRequest

post_detail_url = HyperlinkedIdentityField(view_name='posts-api:postapidetails',lookup_field='slug')

class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id',
                  'title',
                  'content',
                  'publish'
                  ]

class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only =True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id',
                  'title',
                  'user',
                  'content',
                  'html',
                  'image',
                  'publish',
                  'url',
                  'views_count',
                  'comments'
                  ]

    def get_html(self,obj):
        return obj.get_markdown()

    def get_image(self,obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comments(self,obj):
        factory = APIRequestFactory()
        request = factory.get('/')
        serializer_context = {
            'request': Request(request)
        }
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentListSerializer(c_qs, many=True,context=serializer_context).data
        return comments

class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only =True)

    class Meta:
        model = Post
        fields = [
                  'user',
                  'title',
                  'content',
                  'publish',
                  'url',
                  ]


