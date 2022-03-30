from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('add-room', views.AddRoom.as_view(), name='add-room'),
    path('materials', views.MaterialView.as_view(), name='materials')
]
