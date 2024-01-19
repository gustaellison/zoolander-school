from django.urls import path
from . import views
from .views import GradesView, StudentGradesView, create_assignment, AssignmentListView

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_index, name='student_index'),
    path('students/create/', views.StudentCreate.as_view(), name='student_create'),
    path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='student_update'),
    path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='student_delete'),
    path('students/<int:student_id>/', views.student_detail, name="student_detail"),
    path('accounts/signup/', views.signup, name='signup'),
    path('classrooms/<int:classroom_id>/announcement/create/', views.AnnouncementFormView.as_view(), name='announcement_form'),
    path('add_announcement/<int:classroom_id>/', views.add_announcement, name='add_announcement'),
    path('classrooms/', views.ClassroomList.as_view(), name='classrooms_index'),
    path('classrooms/<int:pk>/', views.ClassroomDetail.as_view(), name='classroom_detail'),
    path('classrooms/create/', views.ClassroomCreate.as_view(), name='classroom_create'),
    path('classrooms/<int:pk>/update/', views.ClassroomUpdate.as_view(), name='classroom_update'),
    path('classrooms/<int:pk>/delete/', views.ClassroomDelete.as_view(), name='classroom_delete'),
    path('grades_overview.html', GradesView.as_view(), name='grades_view'),
    path('student/<int:student_id>/', StudentGradesView.as_view(), name='student_grades'),
    path('create_assignment/', create_assignment, name='create_assignment'),
    path('assignment_list/', AssignmentListView.as_view(), name='assignment_list'),
]