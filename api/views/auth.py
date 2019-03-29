from django.contrib.auth.models import User
from rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.admin_user import serializers


class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    @action(methods=['GET'], detail=False, url_path='account')
    def current_user(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)

    # @action(methods=['GET'], detail=False, url_path='account')  # 挺多重复代码
    # def current_user(self, request):
    #     user = UserDetailsView()
    #     user.request = request
    #     user.initial(request=request)
    #     return user.get(user.request)

    @action(methods=['POST'], detail=False, url_path='login', permission_classes=[permissions.AllowAny])
    def login(self, request):
        login_view = LoginView()
        login_view.initial(request=request)
        return login_view.post(request=request)

    @action(methods=['POST'], detail=False, url_path='logout')
    def logout(self, request):
        logout_view = LogoutView()
        logout_view.initial(request=request)
        return logout_view.post(request=request)
