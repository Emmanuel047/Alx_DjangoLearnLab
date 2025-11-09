from atexit import register
from django.template import Library
from django.urls import path
from django.views.generic.list import ListView
from . import views
from .views import list_books, LibraryDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('books/', views.list_books, name='books'),
    path('library/', LibraryDetailView.as_view(), name='LibraryDetailView'),
    path('logout', auth_views.LogoutView.as_view(template_name='relationship_app/templates/logout.html'), name='logout'),
    path('login', auth_views.LoginView.as_view(template_name='relationship_app/templates/login.html'), name='login'),
    path('register', views.register, name='register'),
]