from collections import UserList
from django.db import IntegrityError
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from .models import Student, Classroom, Teacher, Announcement,GradeAssignmentForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import  Assignment, Grade
from .models import AssignmentForm, AssignmentSubmission
from .forms import AnnouncementForm, CommentForm, TeacherForm
from .models import ZoomLinkForm
from .models import AssignmentSubmissionForm
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, Http404,HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
from django import forms

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

@login_required
def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'students/detail.html', {'student': student})

@login_required
def teacher_index(request):
    teachers = Teacher.objects.filter(user=request.user)
    return render(request, 'teachers/index.html', {'teachers': teachers})

def help_index(request):
  return render(request, 'help/index.html')

@login_required
def teacher_detail(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    return render(request, 'teachers/detail.html', {'teacher': teacher})


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      role = request.POST.get('role')
      name = request.POST.get('name')
      try:
        if role == "student":
          student = Student.objects.create(user=user, name=name)
        elif role == 'teacher':
          teacher = Teacher.objects.create(user=user, name=name)
      except Exception as e:
        print(f'Error creating {role} - {str(e)}')
      login(request, user)
      print(request)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class StudentCreate(LoginRequiredMixin,CreateView):
    model = Student
    fields = ['name','email','gpa']

    def form_valid(self, form):
    # Assign the logged in user (self.request.user)
      form.instance.user = self.request.user  
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
            return redirect('submitted_assignments')  
    else:
        form = AssignmentForm()

    return render(request, 'create_assignment.html', {'form': form})    

class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        # Fetch assignments and annotate them with a boolean indicating if a file is submitted
        assignments = Assignment.objects.all()
        for assignment in assignments:
            assignment.has_submitted_file = assignment.submitted_file is not None
        return assignments
    
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
  
class TeacherUpdate(LoginRequiredMixin, UpdateView):
  model = Teacher
  fields = '__all__'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


  
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
    # Ensure the assignment is retrieved correctly, and the student matches the logged-in user
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            assignment.submitted_by_student = True
            assignment.submitted_file = form.cleaned_data['submitted_file']
            assignment.save()
            return redirect('assignment_list')  # Redirect to the list of assignments

    return render(request, 'submit_assignment.html', {'assignment': assignment, 'form': AssignmentSubmissionForm()})




def submitted_assignments_view(request):
    # Fetch all submitted assignments along with grades
    submitted_assignments = Assignment.objects.filter(submitted_by_student=True)
    graded_assignments = Assignment.objects.filter(submitted_by_student=True, grade__isnull=False)

    return render(request, 'submitted_assignments.html', {'submitted_assignments': submitted_assignments, 'graded_assignments': graded_assignments})


def download_file(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Check if the assignment has a submission
    if not assignment.submitted_by_student or not assignment.submissions.exists():
        raise Http404("No assignment submission found for the given assignment ID.")

    # Assuming one submission per assignment for simplicity
    submission = assignment.submissions.first()

    file_path = submission.submitted_file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={submission.submitted_file.name}'
        return response
    


def grade_assignments(request):
    if request.method == 'POST':
        # Handle form submission and update grades
        assignment_ids = request.POST.getlist('assignment_ids')
        grades = request.POST.getlist('grades')

        for assignment_id, grade in zip(assignment_ids, grades):
            assignment = Assignment.objects.get(pk=assignment_id)
            assignment.grade = grade
            assignment.save()

        return redirect('submitted_assignments')  # Redirect to the assignment list or another page

    else:
        # Display a list of submitted assignments for grading
        assignments = Assignment.objects.filter(submitted_by_student=True)
        return render(request, 'grade_assignments.html', {'assignments': assignments})

class GradeAssignmentsView(View):
    template_name = 'grade_assignments.html'

    def get(self, request, assignment_id):
        assignment = Assignment.objects.get(id=assignment_id)
        form = GradeAssignmentForm(instance=assignment)
        return render(request, self.template_name, {'assignment': assignment, 'form': form})

    def post(self, request, assignment_id):
        assignment = Assignment.objects.get(id=assignment_id)
        form = GradeAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('submitted_assignments')

        return render(request, self.template_name, {'assignment': assignment, 'form': form})




    
class GradeAssignmentForm(forms.Form):
    def __init__(self, assignments=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if assignments is not None:
            for assignment in assignments:
                field_name = f"grades_{assignment.id}"
                self.fields[field_name] = forms.DecimalField(
                    label=f"Grade for {assignment.name}",
                    required=True
                )

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation logic if needed
        return cleaned_data




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

