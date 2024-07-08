
from rest_framework import viewsets
from canbanBackend.models import Task, User, SubTask
from canbanBackend.permissions import IsOwnerOrReadOnly
from canbanBackend.serializers import PublicUserSerializer, SubtaskSerializer, TaskSerializer, UserSerializer
from rest_framework import  permissions
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied


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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, 
                          IsOwnerOrReadOnly, permissions.IsAuthenticated] 
    
    def perform_create(self, serializer):
        creator = self.request.user
        request_creator_id = self.request.data.get('creator')
        if request_creator_id and str(request_creator_id) != str(creator.id):
            raise PermissionDenied("You cannot create a task for another user.")
        serializer.save(creator=creator)

    def perform_update(self, serializer):
        creator = self.request.user
        request_creator_id = self.request.data.get('creator')
        if request_creator_id and str(request_creator_id) != str(creator.id):
            raise PermissionDenied("You cannot update the task for another user.")
        serializer.save()
        
class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubtaskSerializer 


class PublicUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer 



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
    