from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    """ ORM модель групп """
    title = models.CharField('Название группы', max_length=200,
                             help_text='Дайте название группе')
    slug = models.SlugField('URL адрес', default='some string',
                            unique=True)
    description = models.TextField('Описание группы',
                                   max_length=10000,
                                   default='some string',
                                   help_text='Описание для группы')

    class Meta:
        """ Metaclass Group """
        verbose_name = 'Группы'
        verbose_name_plural = 'Группы'
        ordering = ('-title',)

    def __str__(self):
        return self.title


class Post(models.Model):
    """ ORM модель постов """
    text = models.TextField('Текст поста', max_length=15000,
                            help_text='Напишите что нибудь...')
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор',)
    group = models.ForeignKey(Group, blank=True, null=True,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              verbose_name='Группа',
                              help_text='Группа поста')

    class Meta:
        """ Metaclass Post """
        ordering = ('-pub_date',)
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[0:15]
