from django.urls import path
from .views import generate_questions_api

urlpatterns = [
    path('generate/', generate_questions_api, name='generate_questions'),
]
