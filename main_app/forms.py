from django.forms import ModelForm
from .models import Announcement, Comment, Teacher

class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description']


class CommentForm(ModelForm):
    class Meta: 
        model = Comment
        fields = ['description']


class TeacherForm(ModelForm):

    class Meta:
        model = Teacher
        fields = ['name', 'email', 'image']
