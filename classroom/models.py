from multiprocessing.reduction import AbstractReducer
import os
import pathlib
import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

def generate_file_code():
    length = 40
    chars = string.ascii_letters + string.digits
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))

def material_directory_path(instance, filename):
        return 'material_file/{0}{1}'.format(generate_file_code(), ''.join(pathlib.Path(filename).suffixes))

def task_directory_path(instance, filename):
        return 'task_file/{0}{1}'.format(generate_file_code(), ''.join(pathlib.Path(filename).suffixes))

class User(AbstractUser):
    pass

class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=3000, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    room_place = models.CharField(max_length=255, blank=True)
    room_code = models.CharField(max_length=12)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')

    def __str__(self):
        return f'{self.name}'

class Material(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=3000, blank=True)
    created_at = models.DateTimeField(blank=True)
    room = models.ForeignKey(Room, default='', on_delete=models.CASCADE, related_name='materials')

    def __str__(self):
        return f'{self.title}'

    def get_comments_lastest_items(self, limit: int):
        comments_count = self.comments.count()
        comments_offset = comments_count - limit
        return self.comments.all()[comments_offset:comments_count]

    def get_comments_lastest_3_items(self):
        return self.get_comments_lastest_items(3)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=3000, blank=True)
    due_datetime = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=now)
    room = models.ForeignKey(Room, default='', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f'{self.title}'

class MaterialFile(models.Model):
    filename = models.CharField(max_length=3000, default='')
    file = models.FileField(upload_to=material_directory_path)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return f'{self.filename}'

    def get_filename(self):
        return os.path.split(self.file.name)[1]

class TaskFile(models.Model):
    filename = models.CharField(max_length=3000, default='')
    file = models.FileField(upload_to=material_directory_path)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return f'{self.filename}'

class MaterialComment(models.Model):
    text = models.CharField(max_length=3000)
    created_at = models.DateTimeField(default=now)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='comments', default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_comments')

    def __str__(self):
        return f'{self.author.username}'

   