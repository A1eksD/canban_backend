
from django.db import models
from canbanBackend.class_assest import PRIORITY_CHOICES
from django.contrib.auth.models import User


class Task(models.Model):
    """
    A model to represent a task in the system.
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True, default='')
    creator = models.ForeignKey('auth.User', related_name='task', on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    assigned_users = models.ManyToManyField(User, related_name='tasks', blank=True)
    category = models.CharField(max_length=20, default='todo')
    
    def __str__(self):
        """
        String representation of the Task object.
        """
        return f'({self.id}) {self.title}'


class SubTask(models.Model):
    """
    A model to represent a subtask related to a main Task.
    """
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the SubTask object.
        """
        return f'({self.id}) {self.name}'

