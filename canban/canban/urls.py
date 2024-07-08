from django.contrib import admin
from django.urls import path, include
from canbanBackend.views import LoginView, LogoutView, register_user



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', register_user, name='register_user'),
    path('api/', include('canbanBackend.urls')),
]

