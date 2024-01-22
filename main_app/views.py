from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from .models import Student, Classroom, Teacher, Announcement
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import  Assignment, Grade
from .models import AssignmentForm
from .forms import AnnouncementForm, CommentForm, TeacherForm
from .models import ZoomLinkForm
from .models import AssignmentSubmissionForm
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

def home_index(request):
    return render(request, 'home.html')

def meeting_index(request):
  return render(request, 'meeting.html')

def add_comment(request, announcement_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.announcement_id = announcement_id
    new_comment.save()
  return redirect('classroom_detail', pk=announcement_id)

class CommentFormView(FormView):
  template_name = 'comment_form.html'
  form_class = CommentForm
  success_url = '/classrooms/'
  def form_valid(self, form):
    announcement_id = self.kwargs['announcement_id']
    return super().form_valid(form)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    announcement_id = self.kwargs.get('announcement_id')
    context['announcement_id'] = announcement_id
    return context

def add_announcement(request, classroom_id):
  form = AnnouncementForm(request.POST)
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
  

def add_profile(request, classroom_id):
  form = TeacherForm(request.POST)
  if form.is_valid():
    new_profile = form.save(commit=False)
    new_profile.classroom_id = classroom_id
    new_profile.save()
  return redirect('classroom_detail', pk=classroom_id)

class TeacherFormView(FormView):
  template_name = 'profile_form.html'
  form_class = TeacherForm
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

def help_index(request):
  return render(request, 'help/index.html')

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
            assignment.teacher = teacher  
            assignment.save()
            return redirect('assignment_list')  
    else:
        form = AssignmentForm()

    return render(request, 'create_assignment.html', {'form': form})    

class AssignmentListView(View):
    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.all()
        return render(request, 'assignment_list.html', {'assignments': assignments})
    
class AssignmentDelete(LoginRequiredMixin, DeleteView):
    model = Assignment
    template_name = 'assignment_confirm_delete.html'  # Create a confirmation template
    success_url = reverse_lazy('assignment_list')  # Redirect to the assignment list after deletion

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj    
    
    
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
  
  def get_success_url(self):
        return reverse('classroom_create')
  
class AnnouncementDelete(DeleteView):
  model = Announcement
  success_url = '/classrooms'

  def get_object(self, queryset=None):
        classroom_id = self.kwargs.get('classroom_id')
        title = self.kwargs.get('title')  
        return get_object_or_404(Announcement, classroom_id=classroom_id, title=title)
  
def meeting_index(request):
    classrooms = Classroom.objects.all()
    return render(request, 'meeting.html', {'classrooms': classrooms}) 

def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, classroom__students=request.user.student)

    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            assignment.submitted_by_student = True
            assignment.submitted_file = form.cleaned_data['submitted_file']
            assignment.save()
            return redirect('assignment_list')  # Redirect to the list of assignments
    else:
        form = AssignmentSubmissionForm()

    return render(request, 'submit_assignment.html', {'assignment': assignment, 'form': form})

# class ClassroomDetail(FormView):
#     template_name = 'classroom_detail.html'
#     form_class = ZoomLinkForm

#     def form_valid(self, form):
#         classroom_id = self.kwargs['pk']
#         classroom = Classroom.objects.get(pk=classroom_id)
#         classroom.zoom_link = form.cleaned_data['zoom_link']
#         classroom.save()
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         classroom_id = self.kwargs.get('pk')
#         context['classroom'] = Classroom.objects.get(pk=classroom_id)
#         return context

