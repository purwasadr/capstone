from multiprocessing.reduction import AbstractReducer
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

# Create your models here.
class User(AbstractUser):
    pass

class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=3000)
    subject = models.CharField(max_length=255, blank=True)
    room_place = models.CharField(max_length=255, blank=True)
    room_code = models.CharField(max_length=12)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')

class Material(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)
    created_at = models.DateTimeField()
    room = models.ForeignKey(Room, default='', on_delete=models.CASCADE, related_name='materials')

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)
    created_at = models.DateTimeField(default=now)
    room = models.ForeignKey(Room, default='', on_delete=models.CASCADE, related_name='tasks')

def material_directory_path(instance, filename):
        return 'material_file_{0}/{1}'.format(instance.material.id, filename)

def task_directory_path(instance, filename):
        return 'task_file_{0}/{1}'.format(instance.task.id, filename)

class MaterialFile(models.Model):
    file = models.FileField(upload_to=material_directory_path)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='files')

class TaskFile(models.Model):
    file = models.FileField(upload_to=material_directory_path)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')

 
