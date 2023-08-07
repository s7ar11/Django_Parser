# parser_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.parse_url, name='parse_url'),
    path('result/', views.result_page, name='result_page'),  # Обновленный URL-шаблон для страницы с результатами
]