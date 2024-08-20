from django import forms
from .models import Review, status
from accounts.models import Lecturer, Student
from document.models import Document


class ReviewUploads(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            'document', 'reviewer', 'status', 'comment', 'student'
        )

    document = forms.ModelChoiceField(label='document', queryset=Document.objects.all())
    reviewer = forms.ModelChoiceField(label='reviewer', queryset=Lecturer.objects.all())
    status = forms.ChoiceField(label='status', choices=status)
    comment = forms.CharField(widget=forms.Textarea)
    student = forms.ModelChoiceField(label='student', queryset=Student.objects.all())



