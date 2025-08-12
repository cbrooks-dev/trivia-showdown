from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get/trivia/data', views.get_trivia_data, name='get_trivia_data'),
    path('get/correct/answer', views.get_correct_answer, name='get_correct_answer'),
]
