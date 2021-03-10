from django.urls import path, include
from apps.users.api.views.user_views import *

urlpatterns = [
    path('create-account/', UserCreateAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('account/', UserRetrieveUpdateAPIView.as_view()),
    # path('users/', UsersList.as_view()),
    # path('users/<int:pk>', UserDetailAPIView.as_view()),
]
