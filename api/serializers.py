import logging
from collections import OrderedDict
from typing import Any

from django.contrib.auth.hashers import make_password
from django.db.models import Model
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from todo import models

logger = logging.getLogger('admin')


# class TodoSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = (
#             'id',
#             'title',
#             'description',
#         )
#         model = models.Todo


class UserSerializer(serializers.ModelSerializer):
    # userId = serializers.IntegerField(source='id', required=False, read_only=True)
    # lastName = serializers.CharField(error_messages={
    #     'required': 'input a last name',
    # }, source='last_name')
    # createTime = serializers.CharField(source='date_joined', required=False)
    # isSuperuser = serializers.BooleanField(source='is_superuser')
    # active = serializers.BooleanField(source='is_active', required=False)
    password = serializers.CharField(
        error_messages={
            'required': 'input a password',
            'blank': 'blank password'
        },
        validators=[
        ],
        # write_only=True,

    )
    username = serializers.CharField(
        error_messages={
            'required': 'input a username',
            'blank': 'blank username',
        },
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='username exist already',
            ),
        ],
    )

    # rolename = serializers.SerializerMethodField()
    # roleId = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'username',
            'password'
        )
        model = User

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance: Model, validated_data: Any):
        validated_data['password'] = make_password(validated_data['password'])
        logger.info(f'testing if the password is correct{validated_data["password"]}')
        instance = super(UserSerializer, self).update(instance, validated_data)
        return instance


class TodoSerializer(serializers.ModelSerializer):
    """rewrite the represent of attributes"""
    todo_id = serializers.IntegerField(source='id', required=False)
    todo_title = serializers.CharField(source='title',
                                       error_messages={  # custom error messages
                                           'required': 'pls, enter the title',
                                           'blank': 'say something?',
                                       })
    # todo_description = serializers.CharField(source='description')

    writer = serializers.SerializerMethodField()

    class Meta:
        model = models.Todo
        # fields = '__all__'
        fields = (
            'id',
            'todo_id',
            'todo_title',
            # 'todo_description',
            'description',
            'writer',
        )
        read_only_fields = ('todo_id',)  # why not working
        extra_kwargs = {
            'description': {  # affects original fields
                'allow_blank': False,
                'write_only': True,
                'error_messages': {
                    'blank': 'blank is not allowed',
                    'required': 'what is it about?'
                },
            },
            'id': {  # as long as original and added into represent fields
                # 'write_only': True,  # AssertionError: May not set both `read_only` and `write_only`
                'default': 'haha',  # when this works
            }
        }

    # def get_roleId(self, obj):
    #     user_id = obj.id
    #     user_to_role = UserToRole.objects.filter(user_id=user_id).first()
    #     return user_to_role.role_id if user_to_role else None

    # def get_rolename(self, obj):
    #     role_id = self.get_roleId(obj)
    #     return Role.objects.filter(id=role_id).first().name if role_id else ''

    # custom attribute, especially from a unrelated table
    def get_writer(self, obj):
        """
        can also get the multiple data from another XxxSerializer()
        >>> return UserSerializer(writer, many=True).data
        notice: param 'writer' needs to be a <QuerySet> object, which is iterable
        :param obj:
        :return:
        """
        name = obj.title
        writer = User.objects.filter(username=name).first()
        return writer.username if writer else None

    def to_representation(self, instance):
        """
        remove the None field from the result
        :param instance:
        :return:
        """
        result = super(TodoSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

    def validate(self, data):
        print(data)
        if data['title'] == data['description']:  # here should use the origin fields' name
            raise serializers.ValidationError("validate test")
        return data

    def validate_todo_id(self, todo_id):
        raise serializers.ValidationError("todo_id is no needed")  # 400 Bad Request when raising sth.

    # def validate_password(self, password):  # seems not working so well
    #     print(password)
    #     if password:
    #         # user.set_password(password)
    #         # user.save()
    #         return password
    #     raise serializers.ValidationError("pls, input pwd")
