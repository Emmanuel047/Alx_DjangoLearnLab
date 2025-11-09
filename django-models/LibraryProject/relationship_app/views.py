from django.shortcuts import render
from django.template import library
from .models import Book, Library
from django.views.generic.list import ListView


# Create your views here.
def mybooks(request):
    books = Book.objects.all()
    return render(request, 'list_books.html')


class lib_detils(ListView):
    model = Library
    template_name= 'library_detail.html'