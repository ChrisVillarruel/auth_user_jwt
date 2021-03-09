# modulos nativos de rest_framework
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Modulos locales
from users.models import User
from detail_error import msg_error
from users.renderers import UserJSONRenderer
from .serializers.login_serializer import LoginSerializer
from .serializers.user_serializer import UserSerializer
from .serializers.logout_serializer import LogoutSerializer
from .serializers.register_serializer import RegistrationSerializer
from .serializers.admin_serializer import UserListSerializer, UserDetailSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = RegistrationSerializer
    permissions_classes = (AllowAny,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        error = msg_error('Error de validación', 'BAD_REQUEST', 400, serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
