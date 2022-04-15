# CS50’s Web Programming with Python and JavaScript

## Classroom
Saya membuat aplikasi seperti Google Classroom. guru dapat membuat kelas, kemiudian memposting materi dan tugas. Sedangkan murid dapat memberi komentar pada postingan materi dan dapat mengumpulkan tugas

## Distinctiveness and Complexity
Meskipun saya membuat aplikasi seperti Google Classroom tetapi tampilan aplikasi saya tidak sepenuhnya sama dengan Google Classroom. Dalam hal kompleksitas, aplikasi ini menggunakan query yang cukup rumit ke database, banyak perubahan tampilan dalam page yang sama, dan ada banyak url route

## Files explanation
* views.py
    * function generate_clas_code for generate class code randomly
    * function context_breadcrumb serves to create a list of breadcrumbs in the dict data type so that the template can directly display it
    * Class AuthView used to redirect page to index if already logged in
    * Class GeneralView serves to check whether the user is logged in or not, if not, it will redirect to the login page
    * Class ClasRouteView serves to check whether the user is included in the member list or whether he is the author in the intended class, otherwise it will return HttpForbidden
    * Class LoginView, RegisterView, and LogoutView used for login, register, and logout
    * Class IndexView used to display the main page
    * Class AddClasView, EditClasView, DeleteClasView for add, edit and delete classes
    * function join_clas for join class with JSON request format
    * Class MaterialsView, AddMaterialView, and DeleteMaterialView serves to display, add, and delete material
    * Class MaterialFileView, TaskFileView, and TaskSubmissionFileView serves to download files of materials, tasks, and task submissions
    * Function material_comment serves to add comments to material posts by accepting requests in JSON format
    * Class TaskView, AddTaskView, and DeleteTaskView for display, add, and delete tasks
    * Class TaskDetailView used to display details of tasks and collect assignments for users who are members
    * Class AddTaskFileView, ChangeTaskFileView, and DeleteTaskFileView berfungsi untuk menambah, mengganti, dan membersihkan file dari penyerahan tugas
    * Class SubmitTaskView dan UnSubmitTaskView berfungsi untuk mensubmit dan menunsubmt tugas
    * Class TaskSubmissionView digunakan untuk menampilkan daftar member yang diberi tugas
    * Class TaskSubmissionDetailView berfungsi untuk menampilkan detail penyerahan yang dilakukan oleh member/murid
    * Class ReturnTaskView berfungsi untuk mengembalikan penyerahan tugas member/murid

* models.py
  Contains all the User, Clas, Material, Task, MaterialFile, TaskFile, MaterialComment, TaskSubmit, TaskSubmitFile models. 

* forms.py
    Terdapat semua form
