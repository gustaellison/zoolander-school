from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_index, name='student_index'),
    path('students/create/', views.StudentCreate.as_view(), name='student_create'),
    path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='student_update'),
    path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='student_delete'),
    path('students/<int:student_id>/', views.student_detail, name="student_detail"),
    path('accounts/signup/', views.signup, name='signup'),
    path('classrooms/', views.ClassroomList.as_view(), name='classrooms_index'),
    path('classrooms/<int:pk>/', views.ClassroomDetail.as_view(), name='classroom_detail'),
]