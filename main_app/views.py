from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def student_index(request):
    return render(request, 'students/index.html')