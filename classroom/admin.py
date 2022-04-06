from django.contrib import admin

from classroom.models import Material, MaterialComment, MaterialFile, Room, Task, TaskFile, User

# Register your models here.
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Material)
admin.site.register(MaterialFile)
admin.site.register(MaterialComment)
admin.site.register(Task)
admin.site.register(TaskFile)
