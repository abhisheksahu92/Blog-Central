#restframeworks
from rest_framework.generics import ListAPIView,UpdateAPIView,CreateAPIView,DestroyAPIView,RetrieveAPIView


#Django Modules
from posts.models import Post
from .serializer import PostSerializer


class PostListApiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCreateApiView(CreateAPIView):
    qs = Post.objects.all()
    pass

class PostUpdateApiView(UpdateAPIView):
    qs = Post.objects.all()
    pass

class PostDeleteApiView(DestroyAPIView):
    qs = Post.objects.all()
    pass

class PostDetailApiView(RetrieveAPIView):
    qs = Post.objects.all()
    pass