import datetime
import json
import os, random, string
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.utils.timezone import now
from django.utils.decorators import method_decorator

from .forms import AddMaterialForm, AddRoomForm, AddTaskForm
from .models import Material, MaterialComment, MaterialFile, Room, Task, TaskFile, User


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

@login_required()
def index(request):
    rooms = Room.objects.all()
    return render(request, 'classroom/index.html', {
        'rooms': rooms
    })

@method_decorator(login_required, name='dispatch')
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
            return HttpResponseRedirect(reverse('index'))
@method_decorator(login_required, name='dispatch')
class MaterialsView(View):
    template_path = 'classroom/materials.html'
    def get(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        materials = Material.objects.filter(room=room_id).order_by('-created_at').all()
        return render(request, self.template_path, {
            'room': room,
            'materials': materials,
            'page': 'materials'
        })
    
    def post(self, request):
        pass

@method_decorator(login_required, name='dispatch')
class AddMaterialView(View):
    template_name = 'classroom/add-material.html'

    def get(self, request, room_id):
        return render(request, self.template_name, {
            'room_id': room_id,
            'form': AddMaterialForm()
        })

    def post(self, request, room_id):
        form = AddMaterialForm(request.POST)
        files = request.FILES.getlist('files')
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
    
            material =  Material.objects.create(title=title, description=description, created_at=now(), room=Room.objects.get(pk=room_id))

            for file in files:
                MaterialFile.objects.create(filename=file.name, file=file, material=material)
            return HttpResponseRedirect(reverse('materials', args=(room_id,)))


def material_file(request, material_id):
    if not request.user.is_authenticated:
        return

    material = MaterialFile.objects.get(pk=material_id)
    file = material.file

    return FileResponse(file, as_attachment=True, filename=material.filename)

def material_comment(request, room_id, material_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must authenticated'}, status=401)
    
    try:
        material = Material.objects.get(pk=material_id)
    except Material.DoesNotExist:
        return JsonResponse({"error": "Material not found."}, status=404)

    if request.method == 'POST':
        data = json.loads(request.body)
        
        if data.get('text') != None:
            MaterialComment.objects.create(
                text=data.get('text'),
                material=material,
                author=request.user
            )
        
        comments = []

        for comment in material.comments.all():
            comments.append({
                'id': comment.id,
                'text': comment.text,
                'created_at': comment.created_at,
                'author': comment.author.username,
            })

        return JsonResponse({
                'success': 'Success add comment',
                'data': comments
            },
            status=201
        )

    comments_json = []

    if request.GET.get('isAll') == 'true':
        comments = material.comments.all()  
    else:
        comments = material.get_comments_lastest_items(3)
    
    for comment in comments:
        comments_json.append({
            'id': comment.id,
            'text': comment.text,
            'created_at': comment.created_at,
            'author': comment.author.username,
        })

    return JsonResponse({
                'success': 'Success',
                'data': comments_json
            },
            status=201
        )

    
class TaskView(View):
    template_name = 'classroom/tasks.html'

    def get(self, request, room_id):
        tasks = Task.objects.filter(room=room_id).order_by('-created_at').all()
       
        return render(request, self.template_name, {
            'room_id': room_id,
            'tasks': tasks,
            'page': 'tasks'
        })

class AddTaskView(View):
    template_name = 'classroom/add-task.html'

    def get(self, request, room_id):
        
        return render(request, self.template_name, {
            'room_id': room_id,
            'form': AddTaskForm(),
        })

    def post(self, request, room_id):
        form = AddTaskForm(request.POST)
        files = request.FILES.getlist('files')
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            date = form.cleaned_data['due_date']
            time = form.cleaned_data['due_time'] or '23:59'

            if date:
                datetime_field = datetime.datetime.fromisoformat(f'{date}T{time}')
            else:
                datetime_field = None
            
            task = Task.objects.create(
                title=title,
                description=description,
                due_datetime=datetime_field,
                room=Room.objects.get(pk=room_id)
            )

            for file in files:
                TaskFile.objects.create(filename=file.name, file=file, task=task)
            return HttpResponseRedirect(reverse('tasks', args=(room_id,)))

class TaskDetailView(View):
    template_name = 'classroom/task-detail.html'

    def get(self, request, room_id, task_id):
        task = get_object_or_404(Task, pk=task_id)
        room = get_object_or_404(Room, pk=room_id)

        return render(request, self.template_name, {
            'room': room,
            'task': task
        })