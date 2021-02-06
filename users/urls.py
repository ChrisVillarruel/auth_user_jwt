from django.urls import path, include
from .api import *

urlpatterns = [
    path('register/', RegistrationAPIView.as_view()),
]
