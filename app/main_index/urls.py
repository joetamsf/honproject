from django.urls import path
from .views import show_main

urlpatterns = [
    path('', show_main),
]