from django.urls import path, include
from apps.users.api.views.user_views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('create-account/', UserCreateAPIView.as_view()),
    path('logout/', LogoutRetrieveDestroyAPIView.as_view()),
    path('account/', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('account-delete/', UserRetrieveDestroyAPIView.as_view()),
]
