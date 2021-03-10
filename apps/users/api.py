# Moduloes de rest_framework
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

# Modulos locales
from detail_error import msg_error
from .renderers import UserJSONRenderer
from .models import User
# from .users.api.serializers.register_serializer import RegistrationSerializer
# from .users.api.serializers.login_serializer import LoginSerializer
# from .users.api.serializers.user_serializer import UserSerializer
# from .users.api.serializers.logout_serializer import LogoutSerializer
# from .users.api.serializers.admin_serializer import UserListSerializer, UserDetailSerializer


class RegistrationAPIView(APIView):
    pass
    # # Permita que cualquier usuario (autenticado o no) llegue a este endpoint.
    # permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    # serializer_class = RegistrationSerializer

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)

    #     # Validaciones
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     error = msg_error('Error de validación', 'BAD_REQUEST', 400, serializer.errors)
    #     return Response(error, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    pass
    # permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    # serializer_class = LoginSerializer

    # def post(self, request):
    #     user = request.data

    #     # Observe aquí que no llamamos `serializer.save ()` como lo hicimos para
    #     # el punto final de registro. Esto es porque no tenemos cualquier cosa para
    #     # salvar. En cambio, el método `validate` en nuestro serializador maneja todo
    #     # lo que necesitamos.
    #     serializer = self.serializer_class(data=user)
    #     if serializer.is_valid():
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     error = msg_error('Error de validación', 'BAD_REQUEST', 400, serializer.errors)
    #     return Response(error, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    pass
    # permission_classes = (IsAuthenticated,)
    # renderer_classes = (UserJSONRenderer,)
    # serializer_class = UserSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     # There is nothing to validate or save here. Instead, we just want the
    #     # serializer to handle turning our `User` object into something that
    #     # can be JSONified and sent to the client.
    #     serializer = self.serializer_class(request.user)

    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     serializer_data = request.data.get('user', {})

    #     # Here is that serialize, validate, save pattern we talked about
    #     # before.
    #     serializer = self.serializer_class(
    #         request.user, data=serializer_data, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_200_OK)


class UsersList(APIView):
    pass
    # permission_classes = (IsAuthenticated, IsAdminUser)
    # serializer_class = UserListSerializer

    # def get(self, request):
    #     query_set = User.objects.all().values('user_id', 'username', 'email', 'is_active')
    #     serializer = self.serializer_class(query_set, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    pass
    # permission_classes = (IsAuthenticated,)
    # serializer_class = LogoutSerializer

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         return Response({'success': 'Sesión Cerrada'}, status=status.HTTP_204_NO_CONTENT)

    #     error = msg_error('Error de validación', 'BAD_REQUEST', 400, serializer.errors)
    #     return Response(error, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    pass
    # permission_classes = (IsAuthenticated, IsAdminUser,)

    # def get_query(self, pk=None):
    #     query_set = User.objects.filter(pk=pk).first()
    #     return query_set

    # # detail movie
    # def get(self, request, pk=None):
    #     query_set = self.get_query(pk)

    #     if query_set is not None:
    #         print(query_set)
    #         serializer = UserDetailSerializer(instance=query_set)
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     error = msg_error('Pelicula no encontrada', 'NOT_FOUND', 404, serializer.errors)
    #     return Response(error, status=status.HTTP_404_NOT_FOUND)
