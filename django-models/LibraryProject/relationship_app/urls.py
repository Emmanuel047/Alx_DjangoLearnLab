from django.template import Library
from django.urls import path
from django.views.generic.list import ListView
from . import views
from .views import Library_DetailView

urlpatterns = [
    path('books/', views.list_books, name='books'),
    path('library/', Library_DetailView.as_view(), name='Library_DetailView')
]