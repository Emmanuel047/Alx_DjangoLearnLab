from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.template import library
from .models import Library
from .models import Book
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView,
from django.contrib.auth.views import LogoutView


# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html')


class LibraryDetailView(ListView):
    model = Library
    template_name= 'relationship_app/library_detail.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = user.CreationForm()
        return render(request, 'relationship_app/templatesregister.html', {'form':form})