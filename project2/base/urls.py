from django.urls import path
from . import views

urlpatterns = [
    path('', views.compare_and_download, name='compare_and_download'),
]
