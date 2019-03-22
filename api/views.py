from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from todo import models
from . import serializers

#
# class ListTodo(generics.ListCreateAPIView):
#     queryset = models.Todo.objects.all()
#     serializer_class = serializers.TodoSerializer
#
#
# class Detail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Todo.objects.all()
#     serializer_class = serializers.TodoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid()  # return boolean value
        serializer.is_valid(raise_exception=True)  # return serializer.errors automatically
        self.perform_create(serializer)
        # try:  # prevent exceptions from database when serializer.is_valid() == True
        #     self.perform_create(serializer)
        # except DatabaseError as e:
        #     return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TodoViewSet(viewsets.ModelViewSet):
    queryset = models.Todo.objects.all()
    serializer_class = serializers.TodoSerializer
