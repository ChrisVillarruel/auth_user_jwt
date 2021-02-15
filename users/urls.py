from django.urls import path, include
from .api import *

urlpatterns = [
    path('register/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', UsersList.as_view()),
    # path('logout/', LogoutAPIView.as_view()),
]
