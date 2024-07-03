
from rest_framework import serializers
from canbanBackend.models import SubTask, Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    
class SubtaskSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = SubTask
        fields = ['id', 'name', 'is_checked']
        
        
class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    subtasks = SubtaskSerializer(many=True)
    assigned_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        assigned_users_data = validated_data.pop('assigned_users')
        task = Task.objects.create(**validated_data)
        for subtask_data in subtasks_data:
            SubTask.objects.create(task=task, **subtask_data)
        task.assigned_users.set(assigned_users_data)  # Verwendung von .set() für Many-to-Many-Feld
        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        assigned_users_data = validated_data.pop('assigned_users')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()

        # Optionale Logik zum Aktualisieren oder Erstellen von SubTasks
        instance.subtasks.all().delete()
        for subtask_data in subtasks_data:
            SubTask.objects.create(task=instance, **subtask_data)

        instance.assigned_users.set(assigned_users_data)  # Verwendung von .set() für Many-to-Many-Feld

        return instance

        
        
        
# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
    
#     def create(self, validated_data):

#         user = User.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#         )

#         return user
#     class Meta:
#         model = User
#         fields = ['username', 'email' , 'password']
#         extra_kwargs = {'password': {'write_only': True}}
        
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         return user
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user