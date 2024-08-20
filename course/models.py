from django.db import models
from djangoProject12.slugify import slugify
from faculty.models import Faculty


# Create your models here.

class Program(models.Model):
    program_name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Program'

    def __str__(self):
        return self.program_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.program_name)
        super(Program, self).save(*args, **kwargs)
