#restframeworks
from rest_framework.generics import ListAPIView,UpdateAPIView,CreateAPIView,DestroyAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.mixins import UpdateModelMixin,DestroyModelMixin
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


#Django Modules
from django.db.models import Q
from comments.models import Comment
from .serializer import CommentListSerializer,CommentDetailSerializer,create_comment_serializer
from .permissions import IsOwnerorReadOnly
from .pagination import CommentLimitOffsetPagination,CommentPageNumberPagination


class CommentCreateApiView(CreateAPIView):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
                model_type=model_type,
                slug=slug,
                parent_id=parent_id,
                user=self.request.user
                )

class CommentDetailApiView(UpdateModelMixin,DestroyModelMixin,RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerorReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CommentListApiView(ListAPIView):
    serializer_class = CommentListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['content','user__first_name']
    pagination_class = CommentPageNumberPagination

    def get_queryset(self):
        qs_list = Comment.objects.all().order_by('timestamp')
        query = self.request.GET.get("q")
        if query:
            qs_list = qs_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return qs_list

#
# class CommentUpdateApiView(RetrieveUpdateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentCreateSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsAuthenticated,IsOwnerorReadOnly]
#
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)



