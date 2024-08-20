from django import forms
from chapter.models import Chapter
from .models import Document


class DocumentUploader(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'content', 'chapter')
        widgets = {'content': forms.FileInput(attrs={'accept': 'application/pdf'})}

    chapter = forms.ModelChoiceField(label='chapter', queryset=Chapter.objects.all(), required=True)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("This field is required.")
        return content