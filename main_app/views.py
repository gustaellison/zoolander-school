from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Student

# Create your views here.

def home(request):
    return render(request, 'home.html')

def student_index(request):
    students = Student.objects.all()
    return render(request, 'students/index.html', {'students': students})

def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'students/detail.html', {'student': student})

class StudentCreate(CreateView):
    model = Student
    fields = '__all__'