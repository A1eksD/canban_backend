from django.urls import path, include
from rest_framework.routers import DefaultRouter
from canbanBackend.views import PublicUserViewSet, SubTaskViewSet, TaskViewSet


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'subtasks', SubTaskViewSet, basename='subtasks')
router.register(r'public_users', PublicUserViewSet, basename='users')

app_name = 'canbanBackend'

urlpatterns = [
    path('', include(router.urls)),
]