from collections import OrderedDict

from rest_framework import serializers
from django.contrib.auth.models import User
from todo import models


# class TodoSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = (
#             'id',
#             'title',
#             'description',
#         )
#         model = models.Todo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'username',
            'password'
        )
        model = User


class TodoSerializer(serializers.ModelSerializer):
    # rewrite the represent of attributes
    todo_id = serializers.IntegerField(source='id')
    todo_title = serializers.CharField(source='title')
    todo_description = serializers.CharField(source='description')

    writer = serializers.SerializerMethodField()

    class Meta:
        # fields = '__all__'
        fields = (
            'todo_id',
            'todo_title',
            'todo_description',
            'writer',
        )
        model = models.Todo

    # def get_roleId(self, obj):
    #     user_id = obj.id
    #     user_to_role = UserToRole.objects.filter(user_id=user_id).first()
    #     return user_to_role.role_id if user_to_role else None

    # def get_rolename(self, obj):
    #     role_id = self.get_roleId(obj)
    #     return Role.objects.filter(id=role_id).first().name if role_id else ''

    # custom attribute, especially from a unrelated table
    def get_writer(self, obj):
        name = obj.title
        writer = User.objects.filter(username=name).first()
        # can also get the multiple data from another XxxSerializer()
        # >>> return UserSerializer(writer, many=True).data
        # notice: param 'writer' needs to be a <QuerySet> object, which is iterable
        return writer.username if writer else None

    # remove the None field from the result
    def to_representation(self, instance):
        result = super(TodoSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
