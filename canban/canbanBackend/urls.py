from django.urls import path, include
from rest_framework.routers import DefaultRouter
from canbanBackend.views import PublicUserViewSet, SubTaskViewSet, TaskViewSet, register_user


# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'subtasks', SubTaskViewSet, basename='subtasks')
router.register(r'public_users', PublicUserViewSet, basename='users')

app_name = 'canbanBackend'

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]