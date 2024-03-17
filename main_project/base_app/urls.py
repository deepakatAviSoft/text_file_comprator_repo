from django.urls import path
from .views import compare_files_view

urlpatterns = [
    path('', compare_files_view, name='compare_files')
]