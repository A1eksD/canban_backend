from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from canban.canbanBackend.views import LoginView, LogoutView, TaskViewSet, UserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
# router.register(r'subtasks', SubTask)
router.register(r'users', UserViewSet , basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]

