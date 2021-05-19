from django.shortcuts import render, redirect
from django.views import generic

from .models import InstagramUserProfile
from .scripts import get_user_info


class HomeView(generic.TemplateView):
    """
    View для главной страницыг. Парсинг одного ника
    """
    template_name = 'home.html'  # html файл который мы видем когда зайдем на страницу

    # post запрос чтобы парсит пользователя
    def post(self, request):
        url = request.POST['profile_url']  # из запроса берем url
        insta_user = get_user_info(url=url)  # отправляем наш url в парсер и ответ получаем объект
        # После окончание запроса для клиента открываем user_info.html и отправляем в эту старницу наш объект чтобы клиент видел результат
        return render(request, template_name='user_info.html', context={'insta_user': insta_user})


class ParserMultipleUsernamesView(generic.TemplateView):
    """
        View для парсинг списка
    """
    template_name = 'parsermultipleusernames.html'  # html файл который мы видем когда зайдем на страницу

    # post запрос чтобы парсит пользователей
    def post(self, request):
        urls = request.POST['profiles_urls']  # из запроса берем список url-ов
        urls = urls.splitlines()  # наш список url-ов разделены по абзацу. Мы их переобразуем в list url-ов
        insta_users_usernames = []  # создаем пустой list чтобы после парсинга туде добавить ник пользователей
        for url in urls:  # создаем цикл, чтобы парсить каждый url отдельно
            if url[:25] == 'https://www.instagram.com':  # проверка url, что он от инстаграма
                insta_user = get_user_info(url=url)  # отправляем наш url в парсер и ответ получаем объект
                insta_users_usernames.append(insta_user.username)  # добавляем ник пользователя в наш пустой список
        # Чтобы показалть результат клиенту мы фильтруем наш модель(таблицу из бд), и возьмем только те объекты которые ник есть в нашем списке 'insta_users_usernames'
        insta_users = InstagramUserProfile.objects.filter(
            username__in=insta_users_usernames)  # insta_users это queryset. Queryset это список объектов заданной модели.
        # Если в insta_users что то есть то для клиента открываем multipleusers_info.html и отправляем в эту старницу наш queryset чтобы клиент видел результат
        if insta_users:
            return render(request, template_name='multipleusers_info.html', context={'insta_users': insta_users})
        # Если insta_users пустой то для клиента возвращаем страница с парсингом списков
        else:
            return redirect('parser_multiple_usernames')
