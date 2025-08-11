from django.shortcuts import render
from django.http import JsonResponse
from . import services

# Create your views here.


def home(request):
    return render(request, 'home.html')

def get_trivia_data(request):
    print(request)
    trivia_data = services.get_trivia_data()
    return JsonResponse(trivia_data)
