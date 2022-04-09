import datetime
import json
import os, random, string
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.utils.decorators import method_decorator

from .forms import AddClasForm, AddMaterialForm, AddTaskForm
from .models import Material, MaterialComment, MaterialFile, Clas, Task, TaskFile, TaskSubmitFile, User


# Create your views here.
def generate_clas_code():
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
    # clases = Clas.objects.filter(Q(author__id=request.user.id) | Q(members__id=request.user.id)).all()
    clases = request.user.clas_members.all().union(request.user.clases.all())
    # clases = Clas.objects.filter(Q(author__id=request.user.id)).all()
    return render(request, 'classroom/index.html', {
        'clases': clases
    })

@method_decorator(login_required, name='dispatch')
class AddClas(View):
    template_path = 'classroom/add-clas.html'

    def get(self, request):
        return render(request, self.template_path, {'form': AddClasForm})
    
    def post(self, request):
        form = AddClasForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            subject = form.cleaned_data['subject']
            room = form.cleaned_data['room']
            clas_code = generate_clas_code()
            Clas.objects.create(
                name = name,
                description = description,
                subject = subject,
                room = room,
                clas_code = clas_code,
                author = request.user
            )
            return HttpResponseRedirect(reverse('index'))
@method_decorator(login_required, name='dispatch')
class MaterialsView(View):
    template_path = 'classroom/materials.html'
    def get(self, request, clas_id):
        clas = get_object_or_404(Clas, pk=clas_id)
        materials = Material.objects.filter(clas=clas_id).order_by('-created_at').all()
        return render(request, self.template_path, {
            'clas': clas,
            'materials': materials,
            'page': 'materials',
            'breadcrumb': context_breadcrumb(request.path, clas)
        })
    
    def post(self, request):
        pass

def context_breadcrumb(request_path: str, clas: Clas):
    list_path = request_path.rsplit('/')
    breadcrumbs = []
    for index, split_path in enumerate(list_path):
        if index == 0:
            breadcrumbs.append({ 'name': 'Home', 'url': reverse('index') })
        elif index == 2:
            if split_path.isdigit():
                breadcrumbs.append({ 'name': clas.name, 'url': reverse('materials', args=(clas.id,)) })
    return breadcrumbs


@method_decorator(login_required, name='dispatch')
class AddMaterialView(View):
    template_name = 'classroom/add-material.html'

    def get(self, request, clas_id):
        return render(request, self.template_name, {
            'clas_id': clas_id,
            'form': AddMaterialForm()
        })

    def post(self, request, clas_id):
        form = AddMaterialForm(request.POST)
        files = request.FILES.getlist('files')
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
    
            material =  Material.objects.create(title=title, description=description, created_at=timezone.now(), clas=Clas.objects.get(pk=clas_id))

            for file in files:
                MaterialFile.objects.create(filename=file.name, file=file, material=material)
            return HttpResponseRedirect(reverse('materials', args=(clas_id,)))


def material_file(request, material_id):
    if not request.user.is_authenticated:
        return

    material = MaterialFile.objects.get(pk=material_id)
    file = material.file

    return FileResponse(file, as_attachment=True, filename=material.filename)

def material_comment(request, clas_id, material_id):
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

    def get(self, request, clas_id):
        tasks = Task.objects.filter(clas=clas_id).order_by('-created_at').all()
       
        return render(request, self.template_name, {
            'clas_id': clas_id,
            'tasks': tasks,
            'page': 'tasks',
        })

class AddTaskView(View):
    template_name = 'classroom/add-task.html'

    def get(self, request, clas_id):
        
        return render(request, self.template_name, {
            'clas_id': clas_id,
            'form': AddTaskForm(),
        })

    def post(self, request, clas_id):
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
                clas=Clas.objects.get(pk=clas_id)
            )

            for file in files:
                TaskFile.objects.create(filename=file.name, file=file, task=task)
            return HttpResponseRedirect(reverse('tasks', args=(clas_id,)))

class TaskDetailView(View):
    template_name = 'classroom/task-detail.html'

    def get(self, request, clas_id, task_id):
        task = get_object_or_404(Task, pk=task_id)
        clas = get_object_or_404(Clas, pk=clas_id)
        submitted_files = task.submitted_files.filter(uploader=request.user)
        is_submitted = task.users_submitted.filter(pk=request.user.id).exists()

        return render(request, self.template_name, {
            'clas': clas,
            'task': task,
            'work_files': submitted_files,
            'is_submitted': is_submitted,
            'is_add': not submitted_files.exists() and not is_submitted,
            'page_name': 'instruction'
        })

class AddTaskSubmitView(View):
    def post(self, request, clas_id, task_id):
        task = Task.objects.get(pk=task_id)
        files = request.FILES.getlist('work-files')

        for file in files:
            TaskSubmitFile.objects.create(filename=file.name, file=file, task=task, uploader=request.user)
        
        return HttpResponseRedirect(reverse('task-detail', args=(clas_id, task_id,)))

@login_required
def join_clas(request):
    if not request.body:
        return JsonResponse({
                'error': 'Body cannot empty',
            },
            status=403
        )
        
    data = json.loads(request.body)
    clas_code = data.get('clas_code')
    search_clas_code = Clas.objects.filter(clas_code=clas_code).first()

    if search_clas_code == None:
        return JsonResponse({
                'error': 'Code not match any class code',
            },
            status=404
        )
    if search_clas_code.members.filter(pk=request.user.id):
        return JsonResponse({
                'error': 'You already join',
            },
            status=404
        )

    if search_clas_code.author.id == request.user.id:
        return JsonResponse({
                'error': 'You author this class',
            },
            status=404
        )

    search_clas_code.members.add(request.user)
    
    return JsonResponse({
                'success': 'Success',
                'data': {
                    'id': search_clas_code.id
                }
            },
            status=201
        )

class AddTaskFileView(View):
    def post(self, request, clas_id, task_id):
        files = request.FILES.getlist('work-files')
        task = Task.objects.get(pk=task_id)

        for file in files:
            TaskSubmitFile.objects.create(filename=file.name, file=file, task=task, uploader=request.user)
        return HttpResponseRedirect(reverse('task-detail', args=(clas_id, task_id)))

class ChangeTaskFileView(View):
    def post(self, request, clas_id, task_id):
        files = request.FILES.getlist('work-files')
        task = Task.objects.get(pk=task_id)

        task.submitted_files.all().delete()

        for file in files:
            TaskSubmitFile.objects.create(filename=file.name, file=file, task=task, uploader=request.user)
        return HttpResponseRedirect(reverse('task-detail', args=(clas_id, task_id)))

class DeleteTaskFileView(View):
    def post(self, request, clas_id, task_id):
        task = Task.objects.get(pk=task_id)

        task.submitted_files.all().delete()

        return HttpResponseRedirect(reverse('task-detail', args=(clas_id, task_id)))

class SubmitTaskView(View):
    def post(self, request, clas_id, task_id):
        task = Task.objects.get(pk=task_id)

        task.users_submitted.add(request.user)

        # return HttpResponseRedirect(reverse('task-detail', args=(clas_id, task_id)))
        return redirect('task-detail', clas_id, task_id, permanent=True)

class UnSubmitTaskView(View):
    def post(self, request, clas_id, task_id):
        task = Task.objects.get(pk=task_id)

        task.users_submitted.remove(request.user)

        # return HttpResponseRedirect(reverse('task-detail', args=(clas_id, task_id)))
        return redirect('task-detail', clas_id, task_id, permanent=True)

class TaskSubmission(View):
    template_name = 'classroom/task-submission.html'

    def get(self, request, clas_id, task_id):
        task = Task.objects.get(pk=task_id)
        clas = Clas.objects.get(pk=clas_id)
        user_submitted = task.users_submitted.all()
        return render(request, self.template_name, {
            'clas': clas,
            'task': task,
            'page_name': 'submission',
            'users_submitted': user_submitted,
            'users_assigned': User.objects.exclude(Q(submitted_tasks=task_id) | Q(clases=task.clas.id)).all()
        })
        # Q(author__id=request.user.id) | Q(members__id=request.user.id)

class TaskSubmissionDetail(View):
    template_name = 'classroom/task-submission-detail.html'
    def get(self, request, clas_id, task_id, user_id):
        task = Task.objects.get(pk=task_id)
        submitted_files = task.submitted_files.filter(uploader=user_id)
        return render(request, self.template_name, {
            'task': task,
            'submitted_files': submitted_files
        })