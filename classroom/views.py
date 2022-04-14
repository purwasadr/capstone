import datetime
import json
import os, random, string
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.humanize.templatetags.humanize import naturaltime

from .forms import ClasForm, MaterialForm, TaskForm
from .models import Material, MaterialComment, MaterialFile, Clas, Task, TaskFile, TaskSubmitFile, User


def generate_clas_code():
    length = 7
    chars = string.ascii_letters
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))

class AuthView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

class GeneralView(View):

    @method_decorator(login_required(redirect_field_name=''))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ClasRouteView(GeneralView):
    
    def dispatch(self, request, *args, **kwargs):
        self.clas = get_object_or_404(Clas, pk=kwargs.get('clas_id'))
        
        if not self.clas.members.filter(pk=request.user.id).exists() and self.clas.author != request.user:
            return HttpResponseForbidden()
        
        return super().dispatch(request, *args, **kwargs)

class LoginView(AuthView):
    def get(self, request):
        return render(request, 'classroom/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, 'Invalid username and/or password.')
            return render(request, 'classroom/login.html')
    
class LogoutView(GeneralView):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

class RegisterView(AuthView):
    def get(self, request):
        return render(request, 'classroom/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']

        password = request.POST['password']
        confirmation = request.POST['confirmation']

        if password != confirmation:
            return render(request, 'classroom/register.html', {
                'message': 'Passwords must match.'
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'classroom/register.html', {
                'message': 'Username already taken.'
            })

        login(request, user)
        return redirect('index')


class IndexView(GeneralView):
    def get(self, request):
        # clases = Clas.objects.filter(Q(author__id=request.user.id) | Q(members__id=request.user.id)).all()
        clases = request.user.clases_owned_and_joined()
        # clases = request.user.clas_members.all().union(request.user.clases.all())
        # clases = Clas.objects.filter(Q(author__id=request.user.id)).all()
        return render(request, 'classroom/index.html', {
            'clases': clases
        })


class AddClas(GeneralView):
    template_path = 'classroom/add-clas.html'

    def get(self, request):
        return render(request, self.template_path, { 'form': ClasForm })
    
    def post(self, request):
        form = ClasForm(request.POST)

        if form.is_valid():
            clas_code = generate_clas_code()
            Clas.objects.create(
                name = form.cleaned_data['name'],
                description = form.cleaned_data['description'],
                section = form.cleaned_data['section'],
                subject = form.cleaned_data['subject'],
                room = form.cleaned_data['room'],
                clas_code = clas_code,
                author = request.user
            )
            return HttpResponseRedirect(reverse('index'))

class EditClasView(ClasRouteView):
    def post(self, request, clas_id):
        clas = self.clas

        if request.user != clas.author:
            return HttpResponseForbidden()

        form = ClasForm(request.POST)
        if form.is_valid():
            clas.name = form.cleaned_data['name']
            clas.description = form.cleaned_data['description']
            clas.section = form.cleaned_data['section']
            clas.subject = form.cleaned_data['subject']
            clas.room = form.cleaned_data['room']
            clas.save()
            return redirect('materials', clas_id)

        return redirect('materials', clas_id)

class DeleteClasView(GeneralView):
    def post(self, request, clas_id):
        clas = get_object_or_404(Clas, pk=clas_id)
        if request.user != clas.author:
            return HttpResponseForbidden()

        clas.delete()
        return redirect('index')
    

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
    searched_clas = Clas.objects.filter(clas_code=clas_code).first()

    if searched_clas == None:
        return JsonResponse({ 'error': 'Code not match any class code' }, status=404)
    if searched_clas.members.filter(pk=request.user.id):
        return JsonResponse({ 'error': 'You already join' }, status=404)

    if searched_clas.author.id == request.user.id:
        return JsonResponse({ 'error': 'You author this class' }, status=404)

    searched_clas.members.add(request.user)
    return JsonResponse({
                'success': 'Success',
                'data': {
                    'id': searched_clas.id
                }
            },
            status=201
        )

class MaterialsView(ClasRouteView):
    template_path = 'classroom/materials.html'
    def get(self, request, clas_id):
        clas = self.clas
        form = ClasForm(initial={ 
                'name': clas.name, 
                'description': clas.description,
                'section': clas.section,
                'subject': clas.subject, 
                'room': clas.room
        })

        materials = Material.objects.filter(clas=clas_id).order_by('-created_at').all()
        return render(request, self.template_path, {
            'clas': clas,
            'materials': materials,
            'page': 'materials',
            'form': form,
            'breadcrumb': context_breadcrumb(request.path, clas)
        })

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


class AddMaterialView(ClasRouteView):
    template_name = 'classroom/add-material.html'

    def get(self, request, clas_id):
        clas = self.clas
        return render(request, self.template_name, {
            'clas': clas,
            'form': MaterialForm()
        })

    def post(self, request, clas_id):
        form = MaterialForm(request.POST)
        files = request.FILES.getlist('files')
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
    
            material =  Material.objects.create(
                title=title,
                description=description,
                created_at=timezone.now(),
                clas=Clas.objects.get(pk=clas_id)
            )

            for file in files:
                MaterialFile.objects.create(filename=file.name, file=file, material=material)
            return HttpResponseRedirect(reverse('materials', args=(clas_id,)))

class MaterialFileView(GeneralView):
    def get(self, request, material_id):
        material = MaterialFile.objects.get(pk=material_id)
        file = material.file

        return FileResponse(file, as_attachment=True, filename=material.filename)

class TaskFileView(GeneralView):
    def get(self, request, task_id):
        task = TaskFile.objects.get(pk=task_id)
        file = task.file

        return FileResponse(file, as_attachment=True, filename=task.filename)

class TaskSubmissionFileView(GeneralView):
    def get(self, request, task_id):
        task_submission_file = get_object_or_404(TaskSubmitFile, pk=task_id)
        file = task_submission_file.file

        return FileResponse(file, as_attachment=True, filename=task_submission_file.filename)


def material_comment(request, clas_id, material_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must authenticated'}, status=401)
    
    try:
        material = Material.objects.get(pk=material_id)
    except Material.DoesNotExist:
        return JsonResponse({'error': 'Material not found.'}, status=404)

    if request.method == 'POST':
        data = json.loads(request.body)
        
        if data.get('text') != None:
            MaterialComment.objects.create(
                text=data.get('text'),
                material=material,
                author=request.user
            )
        return JsonResponse({
                'success': 'Success add comment',
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
            'created_at': naturaltime(comment.created_at),
            'author': comment.author.username,
        })

    return JsonResponse({
                'success': 'Success',
                'data': comments_json,
                'count': material.comments.count()
            },
            status=201
        )

class TaskView(ClasRouteView):
    template_name = 'classroom/tasks.html'

    def get(self, request, clas_id):
        clas = self.clas
        form = ClasForm(initial={ 
                'name': clas.name, 
                'description': clas.description,
                'section': clas.section,
                'subject': clas.subject, 
                'room': clas.room
        })

        tasks = Task.objects.filter(clas=clas_id).order_by('-created_at').all()
       
        return render(request, self.template_name, {
            'clas': clas,
            'form': form,
            'tasks': tasks,
            'page': 'tasks',
        })

class AddTaskView(ClasRouteView):
    template_name = 'classroom/add-task.html'

    def get(self, request, clas_id):
        return render(request, self.template_name, {
            'clas': self.clas,
            'form': TaskForm(),
        })

    def post(self, request, clas_id):
        form = TaskForm(request.POST)
        files = request.FILES.getlist('files')
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            date = form.cleaned_data['due_date']
            time = form.cleaned_data['due_time'] or '23:59'

            if date:
                datetime_field = timezone.make_aware(datetime.datetime.fromisoformat(f'{date}T{time}'))
                # datetime_field = timezone.datetime.fromisoformat(f'{date}T{time}')
            else:
                datetime_field = None
            
            task = Task.objects.create(
                title=title,
                description=description,
                due_datetime=datetime_field,
                clas=self.clas
            )

            for file in files:
                TaskFile.objects.create(filename=file.name, file=file, task=task)
            return HttpResponseRedirect(reverse('tasks', args=(clas_id,)))

class TaskDetailView(GeneralView):
    template_name = 'classroom/task-detail.html'

    def get(self, request, clas_id, task_id):
        task = get_object_or_404(Task, pk=task_id)
        clas = get_object_or_404(Clas, pk=clas_id)
        submitted_files = task.submitted_files.filter(uploader=request.user)
        is_submitted = task.users_submitted.filter(pk=request.user.id).exists()
        is_returned = task.user_task_returned.filter(pk=request.user.id).exists()

        return render(request, self.template_name, {
            'clas': clas,
            'task': task,
            'submission_files': submitted_files,
            'is_submitted': is_submitted,
            'is_add': not submitted_files.exists() and not is_submitted,
            'is_returned': is_returned,
            'page_name': 'instruction'
        })

class AddTaskFileView(GeneralView):
    def post(self, request, clas_id, task_id):
        files = request.FILES.getlist('file-submitted-task')
        task = Task.objects.get(pk=task_id)

        for file in files:
            TaskSubmitFile.objects.create(filename=file.name, file=file, task=task, uploader=request.user)
        return HttpResponseRedirect(reverse('task-detail', args=(clas_id, task_id)))

class ChangeTaskFileView(GeneralView):
    def post(self, request, clas_id, task_id):
        files = request.FILES.getlist('file-submitted-task')
        task = Task.objects.get(pk=task_id)

        task.submitted_files.filter(uploader=request.user).delete()

        for file in files:
            TaskSubmitFile.objects.create(filename=file.name, file=file, task=task, uploader=request.user)
        return HttpResponseRedirect(reverse('task-detail', args=(clas_id, task_id)))

class DeleteTaskFileView(GeneralView):
    def post(self, request, clas_id, task_id):
        task = Task.objects.get(pk=task_id)

        task.submitted_files.filter(uploader=request.user).delete()

        return HttpResponseRedirect(reverse('task-detail', args=(clas_id, task_id)))

class SubmitTaskView(GeneralView):
    def post(self, request, clas_id, task_id):
        task = Task.objects.get(pk=task_id)

        task.users_submitted.add(request.user)

        return redirect('task-detail', clas_id, task_id)

class UnSubmitTaskView(GeneralView):
    def post(self, request, clas_id, task_id):
        task = Task.objects.get(pk=task_id)

        task.users_submitted.remove(request.user)
        return redirect('task-detail', clas_id, task_id, permanent=True)

class TaskSubmissionView(GeneralView):
    template_name = 'classroom/task-submission.html'

    def get(self, request, clas_id, task_id):
        task = Task.objects.get(pk=task_id)
        clas = Clas.objects.get(pk=clas_id)
        user_submitted = task.users_submitted.exclude(returned_task=task).all()
        return render(request, self.template_name, {
            'clas': clas,
            'task': task,
            'page_name': 'submission',
            'users_submitted': user_submitted,
            'users_assigned': task.users_assigned(clas)
            # 'users_assigned': User.objects.exclude(Q(submitted_tasks=task) | Q(clases=task.clas)).filter(clas_members=clas).all()
        })
        # Q(author__id=request.user.id) | Q(members__id=request.user.id)

class TaskSubmissionDetailView(View):
    template_name = 'classroom/task-submission-detail.html'
    def get(self, request, clas_id, task_id, user_id):
        task = Task.objects.get(pk=task_id)
        submitted_files = task.submitted_files.filter(uploader=user_id)
        user_submission = task.clas.members.filter(pk=user_id).first()
        task_user_is_returned = task.user_task_returned.filter(pk=user_id).exists()
        is_user_submit = task.users_submitted.filter(pk=user_id).exists()
        return render(request, self.template_name, {
            'clas_id': clas_id,
            'task_id': task_id,
            'user_id': user_id,
            'task': task,
            'submitted_files': submitted_files,
            'task_user_is_returned': task_user_is_returned,
            'user_submission': user_submission,
            'is_user_submit': is_user_submit
        })

class ReturnTaskView(View):
    def post(self, request, clas_id, task_id, user_id):
        task = Task.objects.get(pk=task_id)
        user = User.objects.get(pk=user_id)
        task.user_task_returned.add(user)

        return redirect('task-submission-detail', clas_id, task_id, user_id)