
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import grade_assignments,  GradesView, StudentGradesView, create_assignment, AssignmentListView, AnnouncementDelete,AssignmentDelete,submit_assignment,submitted_assignments_view,download_file

from .views import  MyGradesView, AnnouncementUpdate

urlpatterns = [
    path('', views.home_index, name='home_index'),
    path('meeting/', views.meeting_index, name='meeting_index'),
    path('students/', views.student_index, name='student_index'),
    path('students/create/', views.StudentCreate.as_view(), name='student_create'),
    path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='student_update'),
    path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='student_delete'),
    path('students/<int:student_id>/', views.student_detail, name="student_detail"),
    path('teachers/', views.teacher_index, name='teacher_index'),
    path('teachers/<int:pk>/update/', views.TeacherUpdate.as_view(), name='teacher_update'),
    path('teachers/<int:teacher_id>/', views.teacher_detail, name="teacher_detail"),
    path('accounts/signup/', views.signup, name='signup'),
    
    path('classrooms/<int:classroom_id>/assoc_classroom/<int:student_id>/', views.assoc_classroom, name='assoc_classroom'),

    path('classrooms/<int:classroom_id>/announcement/create/', views.AnnouncementFormView.as_view(), name='announcement_form'),
    path('add_announcement/<int:classroom_id>/', views.add_announcement, name='add_announcement'),
    path('classrooms/<int:classroom_id>/profile/create/', views.TeacherFormView.as_view(), name='teacher_form'),
    path('add_profile/<int:classroom_id>/', views.add_profile, name='add_profile'),
    path('classrooms/<int:classroom_id>/<str:title>/announcement/delete/', AnnouncementDelete.as_view(), name='announcement_delete'),
    path('classrooms/<int:classroom_id>/<str:title>/announcement/update/', AnnouncementUpdate.as_view(), name='announcement_update'),
    path('classrooms/<int:classroom_id>/<int:announcement_id>/comment/create/', views.CommentFormView.as_view(), name='comment_form'),
    path('classrooms/<int:classroom_id>/<int:announcement_id>/', views.add_comment, name='add_comment'),
    path('classrooms/', views.ClassroomList.as_view(), name='classrooms_index'),
    path('classrooms/<int:pk>/', views.ClassroomDetail.as_view(), name='classroom_detail'),
    path('classrooms/create/', views.ClassroomCreate.as_view(), name='classroom_create'),
    path('classrooms/<int:pk>/update/', views.ClassroomUpdate.as_view(), name='classroom_update'),
    path('classrooms/<int:pk>/delete/', views.ClassroomDelete.as_view(), name='classroom_delete'),
    path('grades_overview.html', GradesView.as_view(), name='grades_view'),
    path('grades/<int:student_id>/', MyGradesView.as_view(), name='my_grades'),
    path('student/<int:student_id>/', StudentGradesView.as_view(), name='student_grades'),
    path('create_assignment/', create_assignment, name='create_assignment'),
    path('assignment_list/', AssignmentListView.as_view(), name='assignment_list'),
    path('assignment/<int:pk>/delete/', AssignmentDelete.as_view(), name='assignment_confirm_delete'),
    path('help/', views.help_index, name='help_index'),
    path('meeting/', views.meeting_index, name='meeting_index'),
    path('assignment/<int:assignment_id>/submit/', submit_assignment, name='submit_assignment'),
    path('submitted_assignments/', submitted_assignments_view, name='submitted_assignments'),
    path('download_file/<int:assignment_id>/', download_file, name='download_file'),
    path('grade_assignments/', grade_assignments, name='grade_assignments'),
    path('students/<int:student_id>/add_photo_student/', views.add_photo_student, name='add_photo_student'),
]