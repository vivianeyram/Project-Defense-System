from django.db import models


# Create your models here.

class Chapter(models.Model):
    chapter_title = models.CharField(max_length=100,  help_text="Chapter One, 2 or 3")
    description = models.TextField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chapter_title
