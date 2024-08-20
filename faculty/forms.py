from django import forms
from .models import Faculty


class FacultyCreationForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = (
            'faculty_name',
        )

