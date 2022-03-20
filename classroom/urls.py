from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/add-room', views.add_room, name='add_room')
]
