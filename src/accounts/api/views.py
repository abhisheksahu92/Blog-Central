#restframeworks
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,UpdateAPIView,CreateAPIView,DestroyAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.mixins import UpdateModelMixin,DestroyModelMixin
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


#Django Modules
from django.db.models import Q
from .serializer import UserCreateSerializer,UserLoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateApiView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.filter(id__gte=0)
    permission_classes = [AllowAny]

class UserLoginApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)