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

def task_submit_directory_path(instance, filename):
        return 'task_submit_file/{0}{1}'.format(generate_file_code(), ''.join(pathlib.Path(filename).suffixes))

class User(AbstractUser):
    pass

class Clas(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=3000, blank=True)
    section = models.CharField(max_length=255, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    room = models.CharField(max_length=255, blank=True)
    clas_code = models.CharField(max_length=12)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clases')
    members = models.ManyToManyField(User, blank=True, related_name='clas_members')

    def __str__(self):
        return self.name

class Material(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=3000, blank=True)
    created_at = models.DateTimeField(blank=True)
    clas = models.ForeignKey(Clas, default='', on_delete=models.CASCADE, related_name='materials')

    def __str__(self):
        return self.title

    def get_comments_lastest_items(self, limit: int):
        if self.comments.count() > limit:
            comments_count = self.comments.count()
            comments_offset = comments_count - limit
            return self.comments.all()[comments_offset:comments_count]
        return self.comments.all()

    def get_comments_lastest_3_items(self):
        return self.get_comments_lastest_items(3)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=3000, blank=True)
    due_datetime = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=now)
    clas = models.ForeignKey(Clas, default='', on_delete=models.CASCADE, related_name='tasks')
    users_submitted = models.ManyToManyField(User, blank=True, through='TaskSubmit', related_name='submitted_tasks')
    user_task_returned = models.ManyToManyField(User, blank=True, related_name='returned_task')

    def __str__(self):
        return self.title

class MaterialFile(models.Model):
    filename = models.CharField(max_length=3000, default='')
    file = models.FileField(upload_to=material_directory_path)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return self.filename

    def get_filename(self):
        return os.path.split(self.file.name)[1]

class TaskFile(models.Model):
    filename = models.CharField(max_length=3000, default='')
    file = models.FileField(upload_to=task_directory_path)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return self.filename

class MaterialComment(models.Model):
    text = models.CharField(max_length=3000)
    created_at = models.DateTimeField(default=now)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='comments', default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_comments')

    def __str__(self):
        return self.author.username

class TaskSubmit(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

class TaskSubmitFile(models.Model):
    filename = models.CharField(max_length=3000, default='')
    file = models.FileField(upload_to=task_submit_directory_path)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submitted_files')
    uploader =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_task_files')

    def __str__(self):
        return self.filename