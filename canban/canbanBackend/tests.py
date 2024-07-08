from django.test import TestCase
from django.contrib.auth.models import User
from canbanBackend.models import Task, SubTask
from canbanBackend.class_assest import PRIORITY_CHOICES
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from canbanBackend.serializers import TaskSerializer, SubtaskSerializer, UserSerializer


#----------------Models-----------------------------------------------
class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            creator=self.user,
            priority=1
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.creator, self.user)
        self.assertEqual(self.task.priority, 1)

    def test_task_str(self):
        self.assertEqual(str(self.task), f'({self.task.id}) Test Task')

class SubTaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            creator=self.user,
            priority=1
        )
        self.subtask = SubTask.objects.create(
            task=self.task,
            name='Test SubTask',
            is_checked=False
        )

    def test_subtask_creation(self):
        self.assertEqual(self.subtask.task, self.task)
        self.assertEqual(self.subtask.name, 'Test SubTask')
        self.assertFalse(self.subtask.is_checked)

    def test_subtask_str(self):
        self.assertEqual(str(self.subtask), f'({self.subtask.id}) Test SubTask')

#----------------Views and Serializers-----------------------------------------------

class UserRegistrationTest(APITestCase):
    def test_register_user(self):
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertTrue('user_id' in response.data)

class TaskViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            creator=self.user,
            priority=1
        )

    def test_list_tasks(self):
        url = reverse('canbanBackend:tasks-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        url = reverse('canbanBackend:tasks-list')
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'priority': 1,
            'subtasks': [],
            'assigned_users': [self.user.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 1)

    def test_update_task(self):
        url = reverse('canbanBackend:tasks-detail', args=[self.task.id])
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': 2,
            'subtasks': [],
            'assigned_users': [self.user.id]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')

class SubTaskViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            creator=self.user,
            priority=1
        )
        self.subtask = SubTask.objects.create(
            task=self.task,
            name='Test SubTask',
            is_checked=False
        )

    def test_list_subtasks(self):
        url = reverse('canbanBackend:subtasks-list') 
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubTask.objects.count(), 1) 
         
    def test_create_subtask(self):
        url = reverse('canbanBackend:subtasks-list') 
        data = {
            'task': self.task.id,
            'name': 'New SubTask',
            'is_checked': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubTask.objects.count(), 2)

    def test_update_subtask(self):
        url = reverse('canbanBackend:subtasks-detail', args=[self.subtask.id])
        data = {
            'task': self.task.id,
            'name': 'Updated SubTask',
            'is_checked': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subtask.refresh_from_db()
        self.assertEqual(self.subtask.name, 'Updated SubTask')
        self.assertEqual(self.subtask.is_checked, True)