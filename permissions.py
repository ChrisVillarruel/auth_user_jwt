# """User permission classes."""

# # Django nativo
# # from django.contrib.auth import is_anonymous

# Django REST Framework
from rest_framework import permissions

# Models
from apps.users.models import User


class IsStandardUser(permissions.BasePermission):
    """Allow access to create experience, extras and proyects."""

    def has_permission(self, request, view):

        # print(request.user.is_superuser)

        if request.user.is_anonymous and request.method == 'POST':
            # Permisos para iniciar sesión o registrase

            return True

        if request.user.is_anonymous and request.method == 'GET':
            return False

        if request.user.is_anonymous and request.method == 'PUT':
            return False

        if request.user.is_anonymous and request.method == 'DELETE':
            return False

        return True
