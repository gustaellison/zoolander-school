from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    image = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    gpa = models.IntegerField(default=0)
    
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
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
