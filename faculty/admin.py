from django.contrib import admin
from .models import Faculty
from course.models import Program
from accounts.models import Student, Lecturer, CustomUser
from reviews.models import Review
from chapter.models import Chapter
from document.models import Document
from project.models import Project

# Register your models here.

admin.site.site_header = "DefensePro Administrator"
admin.site.site_title  = "DefensePro Administrator"
admin.site.index_title = "DefensePro Administrator"


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    search_fields = ['faculty_name']
    list_per_page = 20
    prepopulated_fields = {'slug': ('faculty_name',)}


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    search_fields = ['faculty', 'program_name']
    list_display = ['program_name', 'faculty']
    list_per_page = 20
    prepopulated_fields = {'slug': ('program_name',)}


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'index_number', 'level', 'program')
    list_filter = ('level', 'program')
    search_fields = ('first_name', 'last_name', 'index_number')
    ordering = ('last_name', 'first_name')
    fieldsets = ()
    # prepopulated_fields = {'slug': ('index_number',)}


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ( 'last_name', 'first_name')
    list_filter = ('faculty',)
    search_fields = ('last_name', 'faculty__faculty_name')
    fieldsets = ()
    # prepopulated_fields = {'slug': ('staff_id',)}


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email',  'last_login', 'date_joined')
    list_display_links = ('email',)
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    # Used so the other required fields such as groups is disabled
    filter_horizontal = ()
    list_filter = ()
    # Used to make password read only
    fieldsets = ()


admin.site.register(Review)
admin.site.register(Document)
admin.site.register(Chapter)
admin.site.register(Project)
