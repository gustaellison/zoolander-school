from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from .models import Student, Classroom, Teacher
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import  Assignment, Grade
from .models import AssignmentForm
from .forms import AnnouncementForm
# Create your views here.


class GradesView(View):
    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        overall_gpa = calculate_overall_gpa(students)  # Implement a function to calculate overall GPA

        return render(request, 'grades_overview.html', {'students': students, 'overall_gpa': overall_gpa})

class StudentGradesView(View):
    def get(self, request, student_id, *args, **kwargs):
        student = Student.objects.get(id=student_id)
        assignments = Assignment.objects.filter(student=student)
        grades = Grade.objects.filter(student=student)

        return render(request, 'student_grades.html', {'student': student, 'assignments': assignments, 'grades': grades})
    
def calculate_overall_gpa(students):
    
    total_gpa = sum(student.gpa for student in students)
    overall_gpa = total_gpa / len(students) if students else 0
    return overall_gpa

def home(request):
    return render(request, 'home.html')

def add_announcement(request, classroom_id):
  form = AnnouncementForm(request.POST)
  print(form.data)
  if form.is_valid():
    new_announcement = form.save(commit=False)
    new_announcement.classroom_id = classroom_id
    new_announcement.save()
  return redirect('classroom_detail', pk=classroom_id)

class AnnouncementFormView(FormView):
  template_name = 'announcement_form.html'
  form_class = AnnouncementForm
  success_url = '/classrooms/'
  def form_valid(self, form):
    classroom_id = self.kwargs['classroom_id']
    return super().form_valid(form)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    classroom_id = self.kwargs.get('classroom_id')
    context['classroom_id'] = classroom_id
    return context

@login_required
def student_index(request):
    students = Student.objects.filter(user=request.user)
    return render(request, 'students/index.html', {'students': students})

@login_required
def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'students/detail.html', {'student': student})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      role = request.POST.get('role')
      # This is how we log a user in via code
      if role == "student":
        student = Student.objects.create(user=user)
      elif role == 'teacher':
        teacher = Teacher.objects.create(user=user)
      login(request, user)
      return redirect('/')
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
      return super().form_valid(form)
    
@login_required    
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            teacher = Teacher.objects.get(user=request.user)
            assignment.teacher = teacher  # Assign the logged-in teacher
            assignment.save()
            return redirect('assignment_list')  # Redirect to a page displaying all assignments
    else:
        form = AssignmentForm()

    return render(request, 'create_assignment.html', {'form': form})    

class AssignmentListView(View):
    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.all()
        return render(request, 'assignment_list.html', {'assignments': assignments})
    
    
class StudentUpdate(LoginRequiredMixin, UpdateView):
  model = Student
  fields = '__all__'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class StudentDelete(DeleteView):
  model = Student
  success_url = '/students'
  
class ClassroomDetail(DetailView):
  model = Classroom

class ClassroomList(ListView):
  model = Classroom


class ClassroomUpdate(LoginRequiredMixin, UpdateView):
  model = Classroom
  fields = ['name', 'description', 'schedule']

class ClassroomDelete(LoginRequiredMixin, DeleteView):
  model = Classroom
  success_url = '/classrooms'
  
class ClassroomCreate(LoginRequiredMixin, CreateView):
  model = Classroom
  fields = '__all__'
