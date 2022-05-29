from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Foods

# Create your views here.
@api_view(['GET'])
def show_menu(request):
    menu_dic = {}
    f = Foods.objects.all()

    for _ in range(len(f)):
        menu_dic[(f[_].id)] = f[_].name
  

    return JsonResponse({'menu': menu_dic})