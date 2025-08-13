from django.shortcuts import render
from django.http import JsonResponse
from . import services
import json
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.

@ensure_csrf_cookie
def home(request):
    data = services.get_trivia_data()['results'][0]
    question = data['question']
    choices = []
    choices.append(data['correct_answer'])
    for answer in data['incorrect_answers']:
        choices.append(answer)
    choices.sort()
    return render(request, "home.html", {'question': question, 'choices': choices})


def get_trivia_data(request):
    print(request)
    trivia_data = services.get_trivia_data()
    return JsonResponse(trivia_data)


def get_correct_answer(request):
    data = json.loads(request.body)
    question = data.get('question')
    if not question:
        return JsonResponse({'error': 'Missing "question" parameter'}, status=400)

    result = services.get_correct_answer(question)
    return JsonResponse(result)
