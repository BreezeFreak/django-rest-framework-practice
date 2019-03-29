from django.urls import path, include
from rest_framework import routers

from . import views


# class OptionalSlashRouter(routers.SimpleRouter):
#
#     def __init__(self):
#         self.trailing_slash = '/?'
#         super(routers.SimpleRouter, self).__init__()


# router = OptionalSlashRouter()  # only who registered works
router = routers.DefaultRouter(trailing_slash=True)
# 'trailing_slash=True' no need ending in slash... oops, no working another day
router.register(r'users', views.UserViewSet)
router.register(r'todo', views.TodoViewSet)  # if here is not blank, then 'API Root' showed up.

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_auth.urls')),
    path('register/', include('rest_auth.registration.urls')),

    # # extends from 'viewsets.ModelViewSet', these two views is no needed.
    # path('todo/', views.ListTodo.as_view()),
    # path('todo/<int:pk>/', views.Detail.as_view()),

    # url(r'^users/', include('rest_auth.urls')),  # maybe its registered by router up there, this url doesnt work
]
