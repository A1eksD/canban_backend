# from django.http import HttpResponseRedirect
# from django.shortcuts import redirect, render
from django.forms import ValidationError
from rest_framework import viewsets
from canbanBackend.models import Task, User, SubTask
from canbanBackend.permissions import IsOwnerOrReadOnly
from canbanBackend.serializers import SubtaskSerializer, TaskSerializer, UserSerializer
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     serialized = UserSerializer(data=request.data)
#     if serialized.is_valid():
#         return Response(serialized.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user = serialized.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Dieses ViewSet stellt automatisch `list`, `create`, `retrieve`,
    `update` und `destroy` Aktionen bereit.
    """
    queryset = Task.objects.all() 
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,  # Nur authentifizierte Benutzer können Daten ändern
                          IsOwnerOrReadOnly, IsAuthenticated]  # Benutzer können nur ihre eigenen Snippets ändern
    
    
        
class SubTask(viewsets.ReadOnlyModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubtaskSerializer 

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 



class LoginView(ObtainAuthToken):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

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
    