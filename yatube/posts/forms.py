from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """ Форма создание поста """
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'name': 'Author',
        }
        help_texts = {
            'text': 'Текст поста',
            'group': 'Название группы',
        }
