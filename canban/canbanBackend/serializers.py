
from rest_framework import serializers
from canbanBackend.models import SubTask, Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create and return a new User instance, given the validated data.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    
class SubtaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubTask model.
    """
    class Meta:
        model = SubTask
        fields = ['id', 'name', 'is_checked']
        
        

class PublicUserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying public user information.
    """
    class Meta:
        model = User
        fields = ['id','username']
        
        
        
class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    """
    owner = serializers.ReadOnlyField(source='creator.username')
    subtasks = SubtaskSerializer(many=True)
    assigned_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new Task instance, given the validated data.
        """
        subtasks_data = validated_data.pop('subtasks', [])
        assigned_users = validated_data.pop('assigned_users')
        task = Task.objects.create(**validated_data)
        for subtask_data in subtasks_data:
            SubTask.objects.create(task=task, **subtask_data)
        task.assigned_users.set(assigned_users)
        return task
    
    def update(self, instance, validated_data):
        """
        Update and return an existing Task instance, given the validated data.
        """
        subtasks_data = validated_data.pop('subtasks')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()

        instance.subtasks.all().delete()
        for subtask_data in subtasks_data:
            SubTask.objects.create(task=instance, **subtask_data)

        return instance