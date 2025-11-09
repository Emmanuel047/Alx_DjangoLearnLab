from django.template import Library
from django.urls import path
from django.views.generic.list import ListView
from . import views
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('books/', views.list_books, name='books'),
    path('library/', LibraryDetailView.as_view(), name='LibraryDetailView')
]