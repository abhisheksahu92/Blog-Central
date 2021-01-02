#restframework
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField,SerializerMethodField

#django modules
from posts.models import Post

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
    user = SerializerMethodField()
    image = SerializerMethodField()
    html = SerializerMethodField()
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
                  'views_count'
                  ]

    def get_html(self,obj):
        return obj.get_markdown()

    def get_user(self,obj):
        return str(obj.user.username)

    def get_image(self,obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
                  'user',
                  'title',
                  'content',
                  'publish',
                  'url',
                  ]

    def get_user(self,obj):
        return str(obj.user.username)


