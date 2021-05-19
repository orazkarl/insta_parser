from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'), # url для главной страницы
    path('parser-multiple-usernames', views.ParserMultipleUsernamesView.as_view(), name='parser_multiple_usernames') # url  страницы для парсинга пользователей с списком
]
