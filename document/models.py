from django.core.validators import FileExtensionValidator
from django.db import models
from chapter.models import Chapter
from accounts.models import Student


# Create your models here.

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.FileField(upload_to='documents/%Y/%m/%d/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])
    chapter = models.ForeignKey(Chapter, on_delete=models.RESTRICT)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Document'

    def _str_(self):
        return self.title