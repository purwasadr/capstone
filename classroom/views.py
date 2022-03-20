from django import forms
from django.http import FileResponse
from django.shortcuts import render
from django.core.files.storage import default_storage

class AddRoomForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=3000)
    subject = forms.CharField(max_length=255, required=False)
    room_place = forms.CharField(max_length=255, required=False)


# Create your views here.
def index(request):
    return render(request, 'classroom/index.html')
    # return FileResponse(default_storage.open('material_file_1/Code1.png'))

def add_room(request):
    return render(request, 'classroom/add_room.html', {
        'form': AddRoomForm
    })
