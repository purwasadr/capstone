from django.contrib import admin

from classroom.models import Clas, Material, MaterialComment, MaterialFile, Task, TaskFile, TaskSubmit, TaskSubmitFile, User

# Register your models here.
admin.site.register(User)
admin.site.register(Clas)
admin.site.register(Material)
admin.site.register(MaterialFile)
admin.site.register(MaterialComment)
admin.site.register(Task)
admin.site.register(TaskFile)
admin.site.register(TaskSubmitFile)
admin.site.register(TaskSubmit)

