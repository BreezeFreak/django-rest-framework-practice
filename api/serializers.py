from rest_framework import serializers
from django.contrib.auth.models import User
from todo import models


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
        )
        model = models.Todo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'username',
            'password'
        )
        model = User
