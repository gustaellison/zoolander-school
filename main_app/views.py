from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Student

# Create your views here.

def home(request):
    return render(request, 'home.html')

def student_index(request):
    return render(request, 'students/index.html')

class StudentCreate(CreateView):
    model = Student
    fields = ["name"]