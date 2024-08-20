from django.urls import path
from .views import ListChapter, CreateChapter

app_name = 'chapter'
urlpatterns = [

    path('list/', ListChapter, name='list_chapter_urls'),
    path('new/', CreateChapter, name='new_chapter_urls'),

]
