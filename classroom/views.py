import os, random, string
from webbrowser import get
from django import forms
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.urls import reverse
from django.views import View
from .forms import AddRoomForm
from .models import Material, Room, User
from django.contrib import messages

# Create your views here.
def generate_room_code():
    length = 7
    chars = string.ascii_letters
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, 'Invalid username and/or password.')
            return render(request, 'classroom/login.html')
    else:
        return render(request, "classroom/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "classroom/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "classroom/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'classroom/register.html')

def index(request):
    rooms = Room.objects.all()
    return render(request, 'classroom/index.html', {
        'rooms': rooms
    })
    # return FileResponse(default_storage.open('material_file_1/Code1.png'))


class AddRoom(View):
    template_path = 'classroom/add_room.html'

    def get(self, request):
        return render(request, self.template_path, {'form': AddRoomForm})
    
    def post(self, request):
        form = AddRoomForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            subject = form.cleaned_data['subject']
            room = form.cleaned_data['room_place']
            room_code = generate_room_code()
            Room.objects.create(
                name = name,
                description = description,
                subject = subject,
                room_place = room,
                room_code = room_code,
                author = request.user
            )

class MaterialView(View):
    template_path = 'classroom/materials.html'
    def get(self, request):
        materials = Material.objects.order_by('-created_at').all()
        return render(request, self.template_path, {
            'materials': materials
        })
    
    def post(self, request):
        pass
