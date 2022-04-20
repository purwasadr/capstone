# CS50W Web Programming with Python and JavaScript

## About this app
I created an application similar to Google Classroom. The reason I made this application is because I think this application is quite challenging to make. In this application teachers can create classes, then post materials and assignments. Meanwhile, students can comment on material posts and can submit assignments.

## Distinctiveness and Complexity
Saya yakin aplikasi saya memenuhi persyaratan yang ditentukan karena aplikasi saya berbeda dengan aplikasi sebelumnya yang ada di course ini dalam hal tema, fitur, struktur database, dan kompleksitas . Aplikasi ini dibuat dengan menggunakan Django untuk membuat backend yang terdiri dari 9 model dan banyak halaman. Sedangkan untuk front-end, saya menggunakan Javascript for post, retrieve, and expand comments on material posts, display dialogs and clean up for dues in `add-task.html`, menampilkan dialog untuk mengedit dan menampilkan informasi kelas, and for join classes. 

Even though I made an application like Google Classroom, my application looks not completely the same as Google Classroom. In terms of complexity, this application uses quite complicated queries to the database, many display changes in the same page, and there are many url routes.

## Files explanation
* `classroom` main application directory
  * `admin.py` registering Clas, Material, MaterialComment, MaterialFile, Task, TaskFile, TaskSubmit, TaskSubmitFile and User agar dapat diakses di admin page
  * `views.py`
    * Function `generate_clas_code` for generate class code randomly
    * Function `context_breadcrumb` serves to create a list of breadcrumbs in the dict data type so that the template can directly display it
    * Class `AuthView` used to redirect page to index if already logged in
    * Class `GeneralView` serves to check whether the user is logged in or not, if not, it will redirect to the login page
    * Class `ClasRouteView` serves to check whether the user is included in the member list or whether he is the author in the intended class, otherwise it will return HttpForbidden
    * Class `LoginView`, `RegisterView`, and `LogoutView` used for login, register, and logout
    * Class `IndexView` used to display the main page
    * Class `AddClasView`, `EditClasView`, `DeleteClasView` for add, edit and delete classes
    * Function `join_clas` for join class with JSON request format
    * Class MaterialsView, AddMaterialView, and DeleteMaterialView serves to display, add, and delete material
    * Class MaterialFileView, TaskFileView, and TaskSubmissionFileView serves to download files of materials, tasks, and task submissions
    * Function material_comment serves to add comments to material posts by accepting requests in JSON format
    * Class TaskView, AddTaskView, and DeleteTaskView for display, add, and delete tasks
    * Class TaskDetailView used to display details of tasks and collect assignments for users who are members
    * Class AddTaskFileView, ChangeTaskFileView, and DeleteTaskFileView for add, replace, and clean files from task submission
    * Class SubmitTaskView dan UnSubmitTaskView used for submitting and unsubmitting tasks
    * Class TaskSubmissionView used to display a list of members who were given the task
    * Class TaskSubmissionDetailView serves to display the details of submissions made by members/students
    * Class ReturnTaskView serves to return the assignment of members/students

  * `templates/classroom`
    * `add-clas.html` to display the add class form
    * `add-material.html` to display the add material form
    * `add-task.html` to display the add task form
    * `comment.html` to display the comment view
    * `header-info.html` to display card headers on material and task pages
    * `index.html` to display the main page
    * layout-auth.html to create authorization display section
    * layout-main.html to create the main display section
    * layout.html as base view
    * login.html to display the login form
    * materials.html to display the material list
    * nav-clas.html to navigate between material pages and tasks
    * nav-task.html for navigation between task detail pages and task submission lists
    * register.html to display the registration form
    * task-detail.html to display the details of the task
    * task-submission-detail.html to display the details of the submission
    * task-submission.html to display a list of assignment submissions
    * tasks.html to display task list

  * `models.py`
    * Function `generate_file_code` for generate random filename
    * Function `material_directory_path`, `task_directory_path`, `task_submit_directory_path` for define path and filename
    * `User` model for saving user information
    * `Clas` model for saving class
    * `Material` model for saving material posts
    * `Task` model for saving task posts
    * `MaterialFile` model for save the file information that is in the material
    * `TaskFile` model for save the file information that is in the task
    * `MaterialComment` model for save comments on material posts
    * `TaskSubmit` model for save assignment submission information
    * `TaskSubmitFile` model for save the file information that is in the assignment submission

  * `forms.py` for define forms

  * `urls.py` for all application URLs

  * `static/classroom`
    * `app.js` for post, retrieve, and expand comments on material posts via ajax, display dialogs and clean up for dues in add-task.html, and to join classes via ajax

    * `styles.css` for styling website

* `.gitignore` to ignore files from git

* `capstone`
  * `settings.py`
    * Di `INSTALLED_APPS` saya menambahkan `'classroom'` agar aplikasi saya terdaftar dan `'django_cleanup.apps.CleanupConfig'` untuk mendaftarkan paket django-cleanup ke aplikasi saya
    * `AUTH_USER_MODEL = 'classroom.User'` untuk mengganti model pengguna default ke model pengguna milik saya sendiri
    * `MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')` for change server path to store files in the computer
    * `MEDIA_URL = '/media/'` for change the reference URL for browser to access the files over Http
    * menambakan `LOGIN_URL = '/login'` agar saat menggunakan @loginrequired decorator dapat disesuaikan URL nya
    * `MESSAGE_TAGS = { messages.ERROR: 'danger' }` untuk mengganti error variabel dengan 'danger'
    * `import os`, `from pathlib import Path`, dan `from django.contrib.messages import constants as messages` untuk mengimport package

  * urls.py

## How to run the application
* Install the project dependencies with `pip install -r requirements.txt`
* Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.

## Any other additional information the staff should know
* Naming models, variables, classes, and others that use 'class' names are replaced with 'clas' so as not to conflict with reserved keywords