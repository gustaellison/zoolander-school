from django.urls import path
from . import views
from .views import classroom_details

app_name = 'classroom'

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_index, name='student_index'),
    path('students/create/', views.StudentCreate.as_view(), name='student_create'),
    path('students/<int:id>/', views.student_detail, name="student_detail"),
    path('accounts/signup/', views.signup, name='signup'),
    path('classrooms/<int:classroom_id>/', classroom_details, name='classroom_details'),
]