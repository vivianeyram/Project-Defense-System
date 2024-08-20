from django.db import models
from accounts.models import Lecturer, Student
from document.models import Document

# Create your models here.
status = (
    ('Rejected', 'Rejected'),
    ('Approved', 'Approved'),
    ('Pending', 'Pending.'),
)


class Review(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='reviewers')
    status = models.CharField(choices=status, max_length=20)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="reviewee")

