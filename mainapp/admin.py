from django.contrib import admin # Мы используем готовую админку от Django

from .models import InstagramUserProfile # Импортируем наш модель



@admin.register(InstagramUserProfile) # Регистрируем наш модель чтоб было видно в админ панеле
class InstagramUserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'url', 'biography', 'follow', 'followers', 'full_name'] # Это поля будет видно виде таблицы

    # Сделаем так чтоб никто не смог изменить данные объекта в админ панеле
    def has_change_permission(self, request, obj=None):
        return False

    # И не смог добавить новый объект
    def has_add_permission(self, request):
        return False


from django.contrib.auth.models import Group
admin.site.unregister(Group)