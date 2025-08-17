from django.shortcuts import render
from django.http import JsonResponse
from . import services
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.


@ensure_csrf_cookie
def home(request):
    context_data = services.home()
    return render(
        request,
        "home.html",
        {
            "question": context_data.get("question"),
            "choices": context_data.get("choices"),
        },
    )


def get_new_data(request):
    data = services.get_new_data(request)
    return JsonResponse(data)
