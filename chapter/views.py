from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Chapter
from accounts.decorators import staff_required
from .forms import ChapterCreationForm


# Create your views here.
@staff_required
def ListChapter(request):
    asd = Chapter.objects.all()
    context = {
        'asd': asd,
    }
    return render(request, 'admin/allChapters.html', context)


@staff_required
def CreateChapter(request):
    if request.method == 'POST':
        form = ChapterCreationForm(request.POST)
        if form.is_valid():
            try:
                chapter_add = form.save(commit=False)
                chapter_add.save()
                messages.success(request, 'Chapter added successfully')
                return redirect('chapter:list_chapter_urls')

            except IntegrityError as e:
                messages.error(request, f'Error while saving a new chapter: {e}')
        else:
            messages.error(request, 'Please check the entries in the fields ')
    else:
        form = ChapterCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'admin/newChapter.html', context=context)
