from .models import Program
from django import forms
from faculty.models import Faculty


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = (
            'program_name', 'faculty'
        )

    faculty = forms.ModelChoiceField(label='faculty', queryset=Faculty.objects.all())
    program_name = forms.CharField(label='program name ', max_length=50)


