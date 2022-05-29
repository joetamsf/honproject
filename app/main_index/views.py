from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def show_main(request):
    #Read html file from templates folder
    f = open('main_index/templates/index.html', 'r')
   
    return HttpResponse(f.read())

