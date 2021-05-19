from requests import get
from bs4 import BeautifulSoup as BS
from json import loads

from .models import InstagramUserProfile

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) '}  # юзер агент - маскируем наш парсер под настоящий браузер
cookies = {'urlgen': '"{\"46.211.8.238\": 15895}:1kC5uP:xRV16pq3wjyWtC6J7qf19zOOmCg"',
           'ig_did': '68238712-A08D-431B-9ABF-3EE73106B7AB',
           'shbts': '1607848327.8080251',
           'sessionid': '4852833497%3AmvstRiobJFEm1B%3A9',
           'ig_cb': '1',
           'mid': 'X4Su0wAEAAFsBVnoY9gzVyGKp5Mv',
           'ds_user_id': '4852833497',
           'csrftoken': 'SbmES3m1Hh2NqVwQVX9ZpLDXFKlMABTh',
           'shbid': '19956',
           'rur': 'ATN',
           'fbm_124024574287414': 'base_domain=.instagram.com'}  # Куки - делаем вид что єто не программа а настоящий пользователь


def get_user_info(url):
    url_page = str(url)  # Ссылка на страницу для парсинга
    if 'http://' in url_page or 'https://' in url_page:  # Проверка на наличие протокола в ссылке (есть ли http или https)
        index_username = 3  # Если есть то ставим индекс нужного нам поля 3 (дале пригодится)
    else:
        index_username = 1  # Если нет протокола - индекс 1
    link_data_list = url_page.split('/')  # Разделяем стоку из ссылкой на отдельные элементы с разделителм "/"
    username = link_data_list[
        index_username]  # Получаем юзернейм пользователя из ссылки по индексу (по логике что делали выше.
    # Если был протокол, то юзернейм будет 4 по счету, если нетбыло то вторым)
    response = get(url_page, headers=headers,
                   cookies=cookies)  # Отправляем запрос с юзер агентом и куками инстаграму для получения исходного кода страницы
    status_ask = response.status_code  # Получаем ответ от инстаграма на ошибки (200 - успешно, 404 - страница не найдена и т.д)
    if (status_ask):  # Если ответ 200
        soup = BS(response.text,
                  'html.parser')  # Запускаем парсинг страницы, делаем из исходного кода страницы текст и парсим его
        scripts = soup.find_all('script')  # Находим в коде страцины javascript
        data_script = scripts[4]  # Берем 5 по счету джаваскрипт для обработки
        content = data_script.contents[0]  # В нем берем первый список для дальнейшей обработки
        data_object = content[content.find('{"config"'): -1]  # Находим последний элемент {"config" и передаем все что после него в переменную
        print(content)
        data_json = loads(data_object)  # Делаем из этой переменной JSON
        user_info_json = data_json['entry_data']['ProfilePage'][0]['graphql'][
            'user']  # Переходим в JSON-е к полю юзер - там хранится json с данными пользователя
        # user info to var
        biography = user_info_json['biography']  # Получаем с джейсона биографию пользователя
        followed_by_count = user_info_json['edge_followed_by'][
            'count']  # Получаем с джейсона кол-во подписчиков пользователя
        follow_count = user_info_json['edge_follow']['count']  # Получаем с джейсона кол-во подписок пользователя
        full_name = user_info_json['full_name']  # Получаем с джейсона полное имя пользователя

        # Если данный пользователь уже есть в базе данных то этот объект удаляем и создаем новую
        try:
            InstagramUserProfile.objects.get(username=username).delete()
            insta_user = InstagramUserProfile.objects.create(url=url_page, username=username, biography=biography,
                                                             followers=followed_by_count, follow=follow_count,
                                                             full_name=full_name)
        # Если нет в бд то создаем новую
        except:
            insta_user = InstagramUserProfile.objects.create(url=url_page, username=username, biography=biography,
                                                             followers=followed_by_count, follow=follow_count,
                                                             full_name=full_name)
        # Возвращаем наш объект
        return insta_user
