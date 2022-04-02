from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('add-room', views.AddRoom.as_view(), name='add-room'),
    path('materials/<int:room_id>/add-material', views.AddMaterialView.as_view(), name='add-material'),
    path('materials/<int:room_id>', views.MaterialsView.as_view(), name='materials'),
    path('tasks/<int:room_id>/add', views.AddTaskView.as_view(), name='add-task'),
    path('tasks/<int:room_id>', views.TaskView.as_view(), name='tasks')
]
