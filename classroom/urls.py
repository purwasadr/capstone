from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('add', views.AddClas.as_view(), name='add-clas'),
    path('join', views.join_clas, name='join-clas'),
    path('materials/file/<int:material_id>', views.material_file, name='material-file'),
    path('tasks/file/<int:task_id>', views.material_file, name='task-file'),
    path('<int:clas_id>/edit', views.EditClasView.as_view(), name='edit-clas'),
    path('<int:clas_id>/delete', views.DeleteClasView.as_view(), name='delete-clas'),
    path('<int:clas_id>/materials/add-material', views.AddMaterialView.as_view(), name='add-material'),
    path('<int:clas_id>/materials/<int:material_id>/comments', views.material_comment, name='comments'),
    path('<int:clas_id>/materials', views.MaterialsView.as_view(), name='materials'),
    path('<int:clas_id>/tasks/add', views.AddTaskView.as_view(), name='add-task'),
    path('<int:clas_id>/tasks', views.TaskView.as_view(), name='tasks'),
    path('<int:clas_id>/tasks/<int:task_id>/detail', views.TaskDetailView.as_view(), name='task-detail'),
    path('<int:clas_id>/tasks/<int:task_id>/submission', views.TaskSubmission.as_view(), name='task-submission'),
    path('<int:clas_id>/tasks/<int:task_id>/add-work-file', views.AddTaskFileView.as_view(), name='add-work-file'),
    path('<int:clas_id>/tasks/<int:task_id>/change-work-file', views.ChangeTaskFileView.as_view(), name='change-work-file'),
    path('<int:clas_id>/tasks/<int:task_id>/delete-work-file', views.DeleteTaskFileView.as_view(), name='delete-work-file'),
    path('<int:clas_id>/tasks/<int:task_id>/submit-task', views.SubmitTaskView.as_view(), name='submit-task'),
    path('<int:clas_id>/tasks/<int:task_id>/unsubmit-task', views.UnSubmitTaskView.as_view(), name='unsubmit-task'),
    path('<int:clas_id>/tasks/<int:task_id>/submission/<int:user_id>/detail', views.TaskSubmissionDetail.as_view(), name='task-submission-detail'),
    path('<int:clas_id>/tasks/<int:task_id>/submission/<int:user_id>/return', views.ReturnTaskView.as_view(), name='task-submission-return'),
]
