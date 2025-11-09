from django.template import Library
from django.urls import path
from django.views.generic.list import ListView
from . import views
from .views import lib_detils

urlpatterns = [
    path('books/', views.mybooks, name='books'),
    path('library/', lib_detils.as_view(), name='lib_details')
]