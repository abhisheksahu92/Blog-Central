#restframeworks
from rest_framework.generics import ListAPIView,UpdateAPIView,CreateAPIView,DestroyAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


#Django Modules
from django.db.models import Q

from posts.models import Post
from .serializer import PostListSerializer,PostDetailSerializer,PostCreateSerializer
from .permissions import IsOwnerorReadOnly
from .pagination import PostLimitOffsetPagination,PostPageNumberPagination


class PostCreateApiView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    lookup_field = 'slug'
    #permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetailApiView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

class PostDeleteApiView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerorReadOnly]

class PostListApiView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title','content','user__first_name']
    pagination_class = PostPageNumberPagination
    permission_classes = [AllowAny]
    def get_queryset(self):
        qs_list = Post.objects.all().order_by('-id')
        query = self.request.GET.get("q")
        if query:
            qs_list = qs_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return qs_list


class PostUpdateApiView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerorReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)



