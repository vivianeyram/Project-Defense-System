from django.urls import path
from .views import ListDocuments, addDocs, docDetails

app_name = 'documents'

urlpatterns = [
    path('list/', ListDocuments, name="ListDocuments_urls"),
    path('list/<id>', docDetails, name="Documents_details_urls"),
    path('add/', addDocs, name="newDocuments_urls"),

]
