from django.contrib import admin

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):  # Администрирование постов
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )  # Отображаемые поля поста
    list_editable = ('group',)
    search_fields = ('text',)  # Поиск по тексту
    list_filter = ('pub_date',)  # Фильтрация по дате публикации
    empty_value_display = '-пусто-'  # Если поле пустое


class GroupAdmin(admin.ModelAdmin):  # Администрирование групп
    list_display = (
        'title',
        'slug',
    )  # Отображаемые поля групп
    search_fields = ('title',)  # Поиск по заголовку
    list_filter = ('title',)  # Фильтрация по заголовку


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
