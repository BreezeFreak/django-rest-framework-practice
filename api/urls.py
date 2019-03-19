from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'todo', views.TodoViewSet)  # if here is not blank, then 'API Root' showed up.

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_auth.urls')),
    path('register/', include('rest_auth.registration.urls')),

    # extends from 'viewsets.ModelViewSet', these two views is no needed.
    # path('todo/', views.ListTodo.as_view()),
    # path('todo/<int:pk>/', views.Detail.as_view()),
]
