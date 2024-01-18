from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    image = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    gpa = models.IntegerField(default=0)
    grade = models.IntegerField(default=100)
    address = models.CharField(max_length=300, default='None Listed')
    parents = models.CharField(max_length=200, default='None Listed')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('student_index')
class Assignment(models.Model):
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)    

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    grade = models.DecimalField(max_digits=5, decimal_places=2)

class Teacher(models.Model):
    name = models.CharField(max_length=100)   
    email= models.EmailField(max_length=150)
    image= models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', default=None)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'teacher_id': self.id})
    
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    image= models.CharField(max_length=300)
    schedule = models.DateField('Schedule')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.CharField(max_length=100)
    #teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    