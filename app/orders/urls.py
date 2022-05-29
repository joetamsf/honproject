from django.urls import path
from .views import show_menu

urlpatterns = [
    path('show_menu', show_menu, name='menu'),
]