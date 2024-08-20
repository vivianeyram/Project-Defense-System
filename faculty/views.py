from MySQLdb import IntegrityError
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Faculty
from accounts.decorators import staff_required
from .forms import FacultyCreationForm


# Create your views here.
@staff_required
def listFaculty(request):
    fac = Faculty.objects.all()
    context = {
        'fac': fac

    }
    return render(request, 'admin/faculty.html', context)

@staff_required
def detailsFaculty(request, slug):
    facs = get_object_or_404(Faculty, slug=slug)
    if facs is None:
        raise Http404()
    return render(request, 'admin/facultydetails.html', {'fac': facs})


@staff_required
def addFaculty(request):
    if request.method == 'POST':
        form = FacultyCreationForm(request.POST)
        if form.is_valid():
            try:
                fas = form.save(commit=False)
                fas.save()
                messages.success(request, 'Faculty added  successfully.')
                return redirect('faculty:facultyList_urls')

            except IntegrityError as e:
                messages.error(request, f'An error occurred while adding the Faculty: {e}')
        else:
            messages.error(request, 'Invalid form data. Please check the field.')

    else:
        form = FacultyCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'admin/addFac.html', context)

