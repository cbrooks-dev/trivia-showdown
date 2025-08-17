from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get/new/data', views.get_new_data, name='get_new_data'),
]
