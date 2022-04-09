from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('add-room', views.AddRoom.as_view(), name='add-room'),
    path('room-join', views.join_room, name='room-join'),
    path('materials/file/<int:material_id>', views.material_file, name='material-file'),
    path('<int:room_id>/materials/add-material', views.AddMaterialView.as_view(), name='add-material'),
    path('<int:room_id>/materials/<int:material_id>/comments', views.material_comment, name='comments'),
    path('<int:room_id>/materials', views.MaterialsView.as_view(), name='materials'),
    path('<int:room_id>/tasks/add', views.AddTaskView.as_view(), name='add-task'),
    path('<int:room_id>/tasks', views.TaskView.as_view(), name='tasks'),
    path('<int:room_id>/tasks/<int:task_id>/detail', views.TaskDetailView.as_view(), name='task-detail'),
    path('<int:room_id>/tasks/<int:task_id>/submission', views.TaskSubmission.as_view(), name='task-submission'),
    path('<int:room_id>/tasks/<int:task_id>/add-work-file', views.AddTaskFileView.as_view(), name='add-work-file'),
    path('<int:room_id>/tasks/<int:task_id>/change-work-file', views.ChangeTaskFileView.as_view(), name='change-work-file'),
    path('<int:room_id>/tasks/<int:task_id>/delete-work-file', views.DeleteTaskFileView.as_view(), name='delete-work-file'),
    path('<int:room_id>/tasks/<int:task_id>/submit-task', views.SubmitTaskView.as_view(), name='submit-task'),
    path('<int:room_id>/tasks/<int:task_id>/unsubmit-task', views.UnSubmitTaskView.as_view(), name='unsubmit-task'),
    path('<int:room_id>/tasks/<int:task_id>/submission/<int:user_id>/detail', views.TaskSubmissionDetail.as_view(), name='task-submission-detail'),
]
