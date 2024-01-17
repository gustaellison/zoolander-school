from django.db import models
from django.urls import reverse

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
        return reverse('detail', kwargs={'student_id': self.id})