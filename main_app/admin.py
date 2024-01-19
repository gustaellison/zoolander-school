from django.contrib import admin
from .models import Student, Classroom, Teacher, Announcement

# Register your models here.
admin.site.register(Student)
admin.site.register(Classroom)
admin.site.register(Teacher)
admin.site.register(Announcement)