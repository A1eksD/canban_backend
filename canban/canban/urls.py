from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from canbanBackend.views import LoginView, LogoutView, PublicUserViewSet, TaskViewSet, SubTask, register_user

# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet, basename='tasks')
# router.register(r'subtasks', SubTask, basename='subtasks')
# router.register(r'public_users', PublicUserViewSet , basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('api-auth/', include('rest_framework.urls')),    
    path('register/', register_user, name='register_user'),
    path('api/', include('canbanBackend.urls')),
]

