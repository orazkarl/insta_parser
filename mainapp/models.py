from django.db import models


class InstagramUserProfile(models.Model):
    '''
        Создали модель InstagramUserProfile. Модель будет конвертируется в SQL таблицу, то есть это таблица на нашем базе.
        И в этом таблице есть несколько поля.
    '''
    url = models.CharField(max_length=150, verbose_name='URL адрес пользователя')
    username = models.CharField(max_length=150, verbose_name='Ник пользователя', unique=True)
    biography = models.CharField(max_length=150, verbose_name='Биография пользователя')
    follow = models.IntegerField(verbose_name='Количество подписок пользователя')
    followers = models.IntegerField(verbose_name='Количество подписчиков пользователя')
    full_name = models.CharField(max_length=150, verbose_name='Польное имя пользователя')

    def __str__(self):
        return self.username # Когда вы вызываем объект из таблицы, то нам будет видно ник пользователя

    # Это сделано чтобы в админ панеле было 'Профили пользователей' а не 'InstagramUserProfiles'
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural ='Профили пользователей'