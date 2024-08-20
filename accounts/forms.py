from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student, LevelChoices, Lecturer, LecTitle
from faculty.models import Faculty
from course.models import Program


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    program = forms.ModelChoiceField(label='program', queryset=Program.objects.all())
    supervisor = forms.ModelChoiceField(label='supervisor', queryset=Lecturer.objects.all())
    index_number = forms.CharField(label='Index Number', max_length=15)
    phone = forms.CharField(label='Phone Number', max_length=15)
    level = forms.ChoiceField(label='Level', choices=LevelChoices)


class LecturerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    first_name = forms.CharField(label='First Name', max_length=50)
    title = forms.ChoiceField(label='Title', choices=LecTitle)
    last_name = forms.CharField(label='Last Name', max_length=50)
    staff_id = forms.CharField(label='Staff_Id', max_length=50)
    faculty = forms.ModelChoiceField(label='faculty', queryset=Faculty.objects.all())
    phone = forms.CharField(label='Phone Number', max_length=15)


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'index_number', 'level', 'program', 'phone', 'supervisor')


class LecturerProfileForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ('first_name', 'last_name', 'staff_id', 'phone', 'faculty')
