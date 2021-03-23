# modulos nativos de rest_framework
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Modulos locales
from apps.users.models import User
from apps.users.api.serializers.user_serializer import UserSerializer
from apps.users.api.serializers.login_serializer import LoginSerializer
from type_messages import resource_destroy, logout, resource_updated
from apps.users.api.serializers.register_serializer import RegistrationSerializer
from apps.users.api.serializers.admin_serializer import UserListSerializer, UserDetailSerializer
from permissions import IsStandardUser


class UserCreateAPIView(CreateAPIView):
    """
    Si el registro sale correcto retornara un objeto con los datos
    del usuario y si hay un error, retornara un objeto de tipo error.


    """
    permissions_classes = (IsStandardUser,)
    serializer_class = RegistrationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
    Si el logeo es correcto retornara un objeto con los datos del
    usuario y si hay un error, retornara un objeto de tipo error.


    """
    permissions_classes = [IsStandardUser]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    # Nuevo controlador

    permissions_classes = [IsStandardUser]
    serializer_class = UserSerializer

    def get_queryset(self, email):
        return self.get_serializer().Meta.model.objects.filter(email=email).first()

    def destroy(self, request):
        # Cerrar sesión

        queryset = self.get_queryset(request.user)
        queryset.refresh_token = None
        queryset.access_token = None
        queryset.save()

        return Response(logout(), status=status.HTTP_204_NO_CONTENT)


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permissions_classes = [IsStandardUser]
    serializer_class = UserSerializer

    def get_queryset(self, email):
        if email is not None:
            return self.get_serializer().Meta.model.objects.filter(email=email).first()

    def retrieve(self, request, *args, **kwargs):
        # Muestra información del usuario actual

        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # Actualizar cuenta

        serializer = self.serializer_class(self.get_queryset(request.user), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(resource_updated(), status=status.HTTP_200_OK)

    def destroy(self, request):
        # Suspender cuenta

        user = self.get_queryset(request.user)
        user.state = False
        user.access_token = None
        user.refresh_token = None
        user.save()

        return Response(resource_destroy(), status=status.HTTP_200_OK)


class UserRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    # Eliminar cuenta de manera permanente
    serializer_class = UserSerializer
    permissions_classes = (IsStandardUser,)

    def get_queryset(self, email):
        return self.get_serializer().Meta.model.objects.filter(email=email).first()

    def destroy(self, request):
        queryset = self.get_queryset(request.user).delete()
        return Response(resource_destroy(), status=status.HTTP_200_OK)
