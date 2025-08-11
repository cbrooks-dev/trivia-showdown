from django.shortcuts import render
from django.http import JsonResponse
from . import services

# Create your views here.


def home(request):
    return render(request, 'home.html')

def get_trivia_data(request):
    trivia_data = services.get_trivia_data()
    try:
        request.session['correct_answer'] = trivia_data['results'][0]['correct_answer']
    except Exception as e:
        print(f'Could not parse for correct answer: {e}')
        request.session['correct_answer'] = 'None'
    return JsonResponse(trivia_data)
