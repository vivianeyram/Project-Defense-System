from MySQLdb._exceptions import IntegrityError
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from reviews.models import Review
from .forms import DocumentUploader
from .models import Document
from accounts.models import Student, CustomUser


# Create your views here.


# def ListDocuments(request):
#     try:
#         if request.user.is_staff or request.user.is_lecturer:
#             docs = Document.objects.all()
#         else:
#             docs = Document.objects.filter(student=request.user)
#
#         if not docs.exists() and not (request.user.is_staff or request.user.is_lecturer):
#             return render(request, 'docs/docs_list.html', {'docs': docs})
#         print(docs)
#         return render(request, 'docs/docs_list.html', {'docs': docs})
#
#     except Exception as e:
#         raise Http404()

def ListDocuments(request):
    context = {}

    if request.user.is_staff:
        aocs = Document.objects.all()
        aocs_reviews = {doc.id: doc.reviews.all() for doc in aocs}
        context.update({
            'aocs': aocs,
            'aocs_reviews': aocs_reviews,
        })
    elif hasattr(request.user, 'is_lecturer') and request.user.is_lecturer:
        reviews = Review.objects.filter(reviewer=request.user.lecturer)
        reviewed_docs = Document.objects.filter(reviews__in=reviews).distinct()
        reviewed_docs_reviews = {doc.id: doc.reviews.all() for doc in reviewed_docs}
        context.update({
            'reviewed_docs': reviewed_docs,
            'reviewed_docs_reviews': reviewed_docs_reviews,
        })
    else:
        student = get_object_or_404(Student, user=request.user)
        docs = Document.objects.filter(student=student)
        latest_docs = docs.order_by('-created_at').first()
        docs_reviews = {doc.id: doc.reviews.all() for doc in docs}
        context.update({
            'latest_docs': latest_docs,
            'docs': docs,
            'docs_reviews': docs_reviews,
            'student': student,
        })

    return render(request, 'docs/docs_list.html', context)


def docDetails(request, id):
    try:
        dsdetails = Document.objects.filter(id=id)
        context = {
            'dsdetails': dsdetails
        }
        return render(request, 'docs/dosdetails.html', context)
    except Document.DoesNotExist:
        return Http404()
    except Exception as e:
        return Http404(" An error occurred while processing")


def addDocs(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login_url')

    if request.method == 'POST':
        form = DocumentUploader(request.POST, request.FILES)
        if form.is_valid():
            try:

                document = form.save(commit=False)
                document.student = request.user.student
                document.save()

                messages.success(request, 'Document added successfully.')

                return redirect('documents:ListDocuments_urls')
            except IntegrityError as e:

                messages.error(request, f'An error occurred while adding the document: {e}')
        else:

            print(form.errors)

    else:

        form = DocumentUploader()

    context = {'form': form}
    print(form)
    return render(request, 'docs/adddocs.html', context)
