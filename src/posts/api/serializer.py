#restframework
from rest_framework.serializers import ModelSerializer

#django modules
from posts.models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['title',
                  'content',
                  'publish'
                  ]

