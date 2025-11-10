from re import U
from django.contrib.auth.forms import UserCreationForm
from django.http import request
from django.shortcuts import get_object_or_404, render
from django.template import library
from .models import Library
from .models import Book
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
from relationship_app.models import BookForm
from django.contrib.auth.decorators import permission_required


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
        form = UserCreationForm()
    return render(request, 'relationship_app/templates/register.html', {'form':form})


def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render (request, 'admin_view.html')

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html')

@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_books(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('list_books')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {form: form})


@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_books(request):
    book = get_object_or_404(Book, id=book_id)
    if request.method == '':
        form = BookForm(request.POST, instance=book)
        if form.is_valid:
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return redirect(request, 'book_form.html', {form : form})


@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'book_confirm_delete.html', {'book': book})