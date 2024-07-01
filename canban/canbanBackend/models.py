
from django.db import models
from django.conf import settings

from canbanBackend.class_assest import PRIORITY_CHOICES



class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    
    def __str__(self):
        return f'({self.id}) {self.name}'


class SubTask(models.Model):
    name = models.CharField(max_length=100)
    is_checked = models.BooleanField(default=False)  
        
        
class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True, default='')
    creator = models.ForeignKey('auth.User', related_name='task', on_delete=models.CASCADE, default=1)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    assigned_users = models.ManyToManyField(User, related_name='tasks', blank=True)
    # subtasks = models.ForeignKey(SubTask, related_name='tasks', on_delete=models.CASCADE, default=1)
    subtasks = models.ForeignKey(SubTask, related_name='tasks', on_delete=models.CASCADE, blank=True, null=True)

    # subtasks = models.OneToManyField('SubTask', on_delete=models.CASCADE, default='')


    def __str__(self):
        return f'({self.id}) {self.title}'
    
        
