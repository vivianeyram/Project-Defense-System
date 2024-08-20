from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Lecturer, Student
from document.models import Document
from .models import Review
from .forms import ReviewUploads


# Create your views here.

@login_required
def create_review(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    if request.user.is_lecturer:
        if request.method == 'POST':
            form = ReviewUploads(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.document = document
                lecturer = Lecturer.objects.get(user=request.user)
                review.reviewer = lecturer
                review.save()
                return redirect('documents:Documents_details_urls', document_id=document_id)
        else:
            form = ReviewUploads()

        return render(request, 'create_review.html', {'form': form, 'document': document})
    else:
        return redirect('documents:Documents_details_urls', {'document': document})


def list_reviews(request):
    if request.user.is_authenticated and request.user.is_lecturer:
        lecturer = Lecturer.objects.get(user=request.user)

        reviews = Review.objects.filter(reviewer=lecturer)
    else:
        reviews = []

    return render(request, 'list_reviews.html', {'reviews': reviews})


def student_list_reviews(request):
    if request.user.is_authenticated and request.user.is_student:
        student = Student.objects.get(user=request.user)

        reviews = Review.objects.filter(student=student)
    else:
        reviews = []

    return render(request, 'student_list_reviews.html', {'reviews': reviews})


def all_reviews(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'all_reviews.html', context)
