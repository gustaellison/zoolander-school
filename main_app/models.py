from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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
    classroom = models.ManyToManyField('Classroom', related_name='classroom_relation', symmetrical=False)


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
    classrooms = models.ManyToManyField('Classroom', related_name='classrooms_relation', symmetrical=False)


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

class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    google_drive_link = models.URLField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

class ZoomLinkForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['zoom_link']    


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    grade = models.DecimalField(max_digits=5, decimal_places=2)

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

class Photo(models.Model):
    url = models.CharField(max_length=200)
    # use generic relations to allow a Photo to belong to either a Teacher or a Student
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Photo for {self.content_type} with id {self.object_id} @{self.url}"
