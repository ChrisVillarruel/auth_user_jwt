# users.serializers

from rest_framework import serializers
from rest_framework import exceptions

from apps.users.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'is_active']

    def to_representation(self, instance):
        return {
            'id': instance['user_id'],
            'username': instance['username'],
            'email': instance['email'],
            'is_active': instance['is_active']
        }


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'is_active', 'created_at', 'updated_at']

    def to_representation(self, instance):
        return {
            'username': instance['username'],
            'email': instance['email'],
            'is_active': instance['is_active'],
            'created_at': instance['created_at'].strftime('%A %d. %B %Y'),
            'updated_at': instance['updated_at'].strftime('%A %d. %B %Y')
        }
