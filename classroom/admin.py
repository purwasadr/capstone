from django.contrib import admin

from classroom.models import Material, MaterialFile, Room, User

# Register your models here.
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Material)
admin.site.register(MaterialFile)
