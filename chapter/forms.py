from django import forms
from .models import Chapter


class ChapterCreationForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = (
            'chapter_title', 'description'
        )
