# CS50’s Web Programming with Python and JavaScript

## About this project
Saya membuat aplikasi yang mirip seperti Google Classroom. guru dapat membuat kelas, kemiudian memposting materi dan tugas. Sedangkan murid dapat memberi komentar pada postingan materi dan dapat mengumpulkan tugas

## Distinctiveness and Complexity
Even though I made an application like Google Classroom, my application looks not completely the same as Google Classroom. In terms of complexity, this application uses quite complicated queries to the database, many display changes in the same page, and there are many url routes

## Files explanation
* views.py
    * Function generate_clas_code for generate class code randomly
    * Function context_breadcrumb serves to create a list of breadcrumbs in the dict data type so that the template can directly display it
    * Class AuthView used to redirect page to index if already logged in
    * Class GeneralView serves to check whether the user is logged in or not, if not, it will redirect to the login page
    * Class ClasRouteView serves to check whether the user is included in the member list or whether he is the author in the intended class, otherwise it will return HttpForbidden
    * Class LoginView, RegisterView, and LogoutView used for login, register, and logout
    * Class IndexView used to display the main page
    * Class AddClasView, EditClasView, DeleteClasView for add, edit and delete classes
    * Function join_clas for join class with JSON request format
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

* templates
  * add-clas.html to display the add class form
  * add-material.html to display the add material form
  * add-task.html to display the add task form
  * comment.html to display the comment view
  * header-info.html to display card headers on material and task pages
  * index.html to display the main page
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

* models.py
  Contains all the User, Clas, Material, Task, MaterialFile, TaskFile, MaterialComment, TaskSubmit, TaskSubmitFile models. 

* forms.py for setting forms

* urls.py

* app.js 
  to post, retrieve, and expand comments on material posts via ajax, display dialogs and clean up for dues in add-task.html, and to join classes via ajax

* styles.css
  for styling

## How to run the application
* Install the project dependencies with pip install -r requirements.txt
* Make and apply migrations by running python manage.py makemigrations and python manage.py migrate.

## Any other additional information the staff should know
* Naming models, variables, classes, and others that use 'class' names are replaced with 'clas' so as not to conflict with reserved keywords