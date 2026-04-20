from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Course


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    student_id = forms.CharField(max_length=20)
    full_name = forms.CharField(max_length=100)
    major = forms.CharField(max_length=100)
    year = forms.IntegerField(min_value=1)

    class Meta:
        model = User
        fields = ['username', 'email', 'student_id', 'full_name', 'major', 'year', 'password1', 'password2']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'full_name', 'email', 'major', 'year']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'lecturer', 'credits', 'weekday', 'start_time', 'end_time', 'classroom']