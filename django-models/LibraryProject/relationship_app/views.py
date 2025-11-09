from django.shortcuts import render
from django.template import library
from .models import Library
from .models import Book
from django.views.generic.detail import ListView


# Create your views here.
def mybooks(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html')


class lib_detils(ListView):
    model = Library
    template_name= 'relationship_app/library_detail.html'