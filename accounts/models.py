import requests
from django.contrib import messages
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from decouple import config
from course.models import Program
from djangoProject12.slugify import slugify
from faculty.models import Faculty
from .manager import CustomUserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


LevelChoices = (
    ('1', 'level 100'),
    ('2', 'level 200'),
    ('3', 'level 300'),
    ('4', 'level 400'),
)

LecTitle = (
    ('Dr', 'Doctor'),
    ('Prof', 'Professor'),
    ('Mrs', 'Mrs.'),
    ('Mr', 'Mr.'),

)


class Lecturer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(choices=LecTitle, max_length=25, blank=True, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=11, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.RESTRICT, related_name="Staff_faculty")

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    index_number = models.CharField(max_length=15, validators=[
        RegexValidator(regex=r"^\w{2}\d{8}$", message='Enter a valid pattern like CS20200015',
                       ),
    ],
                                    help_text='Format: CS20200015'

                                    )
    level = models.CharField(max_length=15, choices=LevelChoices, help_text='your student level', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.RESTRICT, related_name='students_course', blank=True, null=True)
    supervisor = models.ForeignKey(Lecturer, on_delete=models.RESTRICT, related_name='Supervisor', blank=True,
                                   null=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserAgentInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_agent = models.CharField(max_length=255)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    ip_country = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.user_agent}"

    def save(self, *args, **kwargs):
        if self.user_ip and not self.ip_country:
            self.ip_country = self.get_country_from_ip()
        super().save(*args, **kwargs)

    def get_country_from_ip(self):
        if self.user_ip:
            api_key = config('IPSTACK_API_KEY', default='')
            api_url = f'http://api.ipstack.com/{self.user_ip}?access_key={api_key}'

            try:
                response = requests.get(api_url)
                data = response.json()
                country_name = data.get('country_name')
                return country_name
            except requests.RequestException as e:
                messages.error(f"Error in get_country_from_ip: {e}")

                return None
