from django.shortcuts import render,redirect
<<<<<<< HEAD
from django.views.generic.edit import CreateView
from .models import Student, Classroom
=======
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Student
>>>>>>> 83b2dcd399baf3f96228d8b95c3f294211652c32
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def student_index(request):
    students = Student.objects.filter(user=request.user)
    return render(request, 'students/index.html', {'students': students})

@login_required
def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'students/detail.html', {'student': student})

def spanish_page(request):
    # Add any logic you need for the Spanish class page
    return render(request, 'classes/spanish.html')

def reading_page(request):
    # Add any logic you need for the Spanish class page
    return render(request, 'classes/reading.html')

def science_page(request):
    # Add any logic you need for the Spanish class page
    return render(request, 'classes/science.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('student_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class StudentCreate(LoginRequiredMixin,CreateView):
    model = Student
    fields = ['name','email','gpa']

    def form_valid(self, form):
    # Assign the logged in user (self.request.user)
      form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
<<<<<<< HEAD
     return super().form_valid(form)
   
def classroom_details(request):
    # Retrieve a classroom instance, you can modify this based on your logic
    classroom_instance = Classroom.objects.first()
    return render(request, 'classrooms/detail.html', {'classroom': classroom_instance})
=======
      return super().form_valid(form)
    
class StudentUpdate(LoginRequiredMixin, UpdateView):
  model = Student
  fields = '__all__'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class StudentDelete(DeleteView):
  model = Student
  success_url = '/students'
>>>>>>> 83b2dcd399baf3f96228d8b95c3f294211652c32
