from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django import forms
from django.views import View
from django.shortcuts import render,redirect
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    image = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    gpa = models.IntegerField(default=0)
    grade = models.IntegerField(default=100)
    address = models.CharField(max_length=300, default='None Listed')
    parents = models.CharField(max_length=200, default='None Listed')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    classroom = models.ManyToManyField('Classroom', related_name='classroom_relation', symmetrical=False, blank=True)
    photos = GenericRelation('main_app.Photo')


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('student_index')
    
    
class Teacher(models.Model):
    name = models.CharField(max_length=100)   
    email= models.EmailField(max_length=150)
    image= models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', default=None)
    classrooms = models.ManyToManyField('Classroom', related_name='classrooms_relation', symmetrical=False, blank=True)
    photos = GenericRelation('main_app.Photo')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'teacher_id': self.id})    
    
    def get_absolute_url(self):
        return reverse('teacher_index')    
    
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    image= models.CharField(max_length=300)
    schedule = models.DateField('Schedule')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # students = models.ManyToManyField(Student)
    students = models.ManyToManyField('Student', related_name='student_relation', symmetrical=False)
    # teacher = models.CharField(max_length=100, default="no teacher")
    # teachers = models.ManyToManyField(Teacher)
    teachers = models.ManyToManyField('Teacher', related_name='teacher_relation', symmetrical=False)

    zoom_link = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('classroom_detail', args=[str(self.id)])
    
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    grade = models.DecimalField(max_digits=5, decimal_places=2)    

class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    google_drive_link = models.URLField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    submitted_by_student = models.BooleanField(default=False)
    submitted_file = models.FileField(upload_to='assignment_submissions/', null=True, blank=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    graded = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ZoomLinkForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['zoom_link']   

class AssignmentSubmissionForm(forms.Form):
    submitted_file = forms.FileField(required=False)       




class AssignmentForm(forms.ModelForm):
    google_drive_link = forms.URLField(label='Google Drive Link', required=False)
    class Meta:
        model = Assignment
        fields = ['student', 'teacher', 'classroom', 'name', 'google_drive_link', 'due_date']  

    

    
class Announcement(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, default=None)
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=300, default=None)

    class Meta: 
        ordering = ['-created_at']

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='submissions/')       

    def __str__(self):
        return f"{self.student.name}'s submission for {self.assignment.name}" 
    

class GradeAssignmentForm(forms.Form):
    grades = forms.DecimalField(label='Grades', required=True)

    class Meta:
        model = Assignment
        fields = ['grade']

    def clean(self):
        cleaned_data = super().clean()
        grades_data = cleaned_data.get('grades')

        if grades_data is None:
            raise forms.ValidationError("No grades provided.")

        return cleaned_data
            
class SubmittedAssignmentsView(View):
    template_name = 'submitted_assignments.html'

    def get(self, request, *args, **kwargs):
        # Fetch all submitted assignments
        submitted_assignments = Assignment.objects.filter(submitted_by_student=True)

        # Provide the link or button for grading assignments
        grade_assignments_url = reverse('grade_assignments')
        grade_form = GradeAssignmentForm()

        return render(request, self.template_name, {
            'submitted_assignments': submitted_assignments,
            'grade_assignments_url': grade_assignments_url,
            'grade_form': grade_form,
            'grades_data': request.GET.get('grades_data', ''),  # Pass the grades_data to the template
        })

    def post(self, request, *args, **kwargs):
        # Handle form submission to assign grades
        grade_form = GradeAssignmentForm(request.POST)

        if grade_form.is_valid():
            grades_data = grade_form.cleaned_data['grades']

            # Loop through assignments and create/update grades
            for assignment_id in request.POST.getlist('assignments'):
                assignment = Assignment.objects.get(pk=assignment_id)

                # Create or update the grade for the assignment
                grade, created = Grade.objects.get_or_create(student=assignment.student, defaults={'grade': grades_data})

                if not created:
                    grade.grade = grades_data
                    grade.save()

                # Mark the assignment as graded
                assignment.graded = True
                assignment.grade = grade
                assignment.save()

            return redirect('submitted_assignments')

        # If the form is not valid, render the page with error messages
        return render(request, self.template_name, {
            'submitted_assignments': Assignment.objects.filter(submitted_by_student=True),
            'grade_assignments_url': reverse('grade_assignments'),
            'grade_form': grade_form,
        })
class Photo(models.Model):
    url = models.CharField(max_length=200)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for student_id: {self.student_id} @{self.url}"
    
    def __str__(self):
        return f"Photo for teacher_id: {self.teacher_id} @{self.url}"
