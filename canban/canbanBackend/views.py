from django.shortcuts import render
from rest_framework import viewsets
from canbanBackend.models import Task, User
from canbanBackend.permissions import IsOwnerOrReadOnly
from canbanBackend.serializers import SubtaskSerializer, TaskSerializer, UserSerializer
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import logout


class TaskViewSet(viewsets.ModelViewSet):  # Definition eines ModelViewSets für Snippets
    """
    Dieses ViewSet stellt automatisch `list`, `create`, `retrieve`,
    `update` und `destroy` Aktionen bereit.
    """
    queryset = Task.objects.all() 
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,  # Nur authentifizierte Benutzer können Daten ändern
                          IsOwnerOrReadOnly]  # Benutzer können nur ihre eigenen Snippets ändern


# class SubTask(viewsets.ReadOnlyModelViewSet):
#     queryset = SubTask.objects.all()
#     serializer_class = SubtaskSerializer 

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 



class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response({'message': 'Logout successful'})