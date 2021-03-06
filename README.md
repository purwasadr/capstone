# CS50W Web Programming with Python and JavaScript

## About this app
I created an application similar to Google Classroom. Even though I made an application like Google Classroom, my application looks not completely the same as Google Classroom. The reason I made this application is because I think this application is quite challenging to make. In this application teachers can create classes, then post materials and assignments. Meanwhile, students can comment on material posts and can submit assignments.

## Distinctiveness and Complexity
I believe my application meets the specified requirements because it differs from the other projects in this course in terms of themes, features, and database structure. As for the theme, my application has a theme about education which is of course different from other projects in this course. In terms of features, this application has several features such as creating classes, adding tasks (for teachers/authors), adding materials (for teachers/authors), submit tasks (for students/members), commenting on material posts, and returning tasks (for teachers/authors). In addition, this application database has a structure that has a different level of difficulty from the other projects in this course, so there is the use of `OR` and `UNION` in this application's database queries.

This application was built using Django to create a backend consisting of 9 models, 33 routes, and many pages. For the front-end, I use Javascript to post, retrieve, and expand comments on material posts, display dialogs and clear dues in `add-task.html`, display dialogs for editing and displaying class information, and for joining classes. All pages in this application are mobile-responsive using Bootstrap and CSS

## Files explanation
* `classroom` main application directory
  * `admin.py` for registration of `Class`, `Material`, `MaterialComment`, `MaterialFile`, `Task`, `TaskFile`, `TaskSubmit`, `TaskSubmitFile` and `User` models for access in admin page
  * `views.py` application views
    * Function `generate_clas_code` for generate class code randomly
    * Function `context_breadcrumb` serves to create a list of breadcrumbs in the dict data type so that the template can directly display it
    * Class `AuthView` used to redirect page to index if already logged in
    * Class `GeneralView` serves to check whether the user is logged in or not, if not, it will redirect to the login page
    * Class `ClasRouteView` serves to check whether the user is included in the member list or whether he is the author in the intended class, otherwise it will return HttpForbidden
    * Class `LoginView`, `RegisterView`, and `LogoutView` used for login, register, and logout
    * Class `IndexView` used to display the main page
    * Class `AddClasView`, `EditClasView`, `DeleteClasView` for add, edit and delete classes
    * Function `join_clas` for join class with JSON request format
    * Class `MaterialsView`, `AddMaterialView`, and `DeleteMaterialView` serves to display, add, and delete material
    * Class `MaterialFileView`, `TaskFileView`, and `TaskSubmissionFileView` serves to download files of materials, tasks, and task submissions
    * Function `material_comment` serves to add comments to material posts by accepting requests in JSON format
    * Class `TaskView`, `AddTaskView`, and `DeleteTaskView` for display, add, and delete tasks
    * Class `TaskDetailView` used to display details of tasks and collect assignments for users who are members
    * Class `AddTaskFileView`, `ChangeTaskFileView`, and `DeleteTaskFileView` for add, replace, and clean files from task submission
    * Class `SubmitTaskView` dan `UnSubmitTaskView` used for submitting and unsubmitting tasks
    * Class `TaskSubmissionView` used to display a list of members who were given the task
    * Class `TaskSubmissionDetailView` serves to display the details of submissions made by members/students
    * Class `ReturnTaskView` serves to return the assignment of members/students
  * `templates/classroom` contains application templates
    * `add-clas.html` to display the add class form
    * `add-material.html` to display the add material form
    * `add-task.html` to display the add task form
    * `comment.html` to display the comment view
    * `header-info.html` to display card headers on material and task pages
    * `index.html` to display the main page
    * `layout-auth.html` to create authorization display section
    * `layout-main.html` to create the main display section
    * `layout.html` as base view
    * `login.html` to display the login form
    * `materials.html` to display the material list
    * `nav-clas.html` to navigate between material pages and tasks
    * `nav-task.html` for navigation between task detail pages and task submission lists
    * `register.html` to display the registration form
    * `task-detail.html` to display the details of the task
    * `task-submission-detail.html` to display the details of the submission
    * `task-submission.html` to display a list of assignment submissions
    * `tasks.html` to display task list
  * `models.py` contains Django Models
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
  * `static/classroom` contains static content
    * `app.js` for post, retrieve, and expand comments on material posts via ajax, display dialogs and clean up for dues in add-task.html, and to join classes via ajax
    * `styles.css` for styling website
* `capstone` project directory
  * `settings.py` contains project settings
    * In `INSTALLED_APPS` i added `'classroom'` to register my app, `'django_cleanup.apps.CleanupConfig'` to register django-cleanup package to my app, and `'django.contrib.humanize'` for register Django template filters
    * `AUTH_USER_MODEL = 'classroom.User'` to change the default user model to my own user model
    * `MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')` to change the server path to save files on the computer
    * `MEDIA_URL = '/media/'` to change the reference URL for the browser to access files via Http
    * `LOGIN_URL = '/login'` overrides the URL or named URL pattern where the request is redirected to login when using the `login_required()` decorator
    * `MESSAGE_TAGS = { messages.ERROR: 'danger' }` for change the default tags for message level
    * `import os`, `from pathlib import Path`, and `from django.contrib.messages import constants as messages` to import packages
  * `urls.py`
    * I added `path('', include('classroom.urls'))` to include my app's URLConf
* `.gitignore` to ignore files from git
* `requirements.txt` list all of the modules need for Django project to work

## How to run the application
* Install the project dependencies with `pip install -r requirements.txt`
* Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.

## Any other additional information the staff should know
* Naming models, variables, classes, and others that use 'class' names are replaced with 'clas' so as not to conflict with reserved keywords
* django-cleanup package is used to automatically deletes files for FileField, ImageField and subclasses