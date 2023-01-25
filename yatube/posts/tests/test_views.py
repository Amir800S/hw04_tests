from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from .fixtures import models
from ..forms import PostForm
from ..models import Post


class TaskPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.post = models.post()
        cls.second_group = models.second_group()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def what_is_in_context(self, request, args, get_cont=False):
        """ Функция проверки контекста View"""
        if get_cont:
            response = self.authorized_client.get(reverse(request, args=args))
            post = response.context['onepost']
        else:
            response = self.authorized_client.get(reverse(request, args=args))
            post = response.context['page_obj'][0]
        self.assertEqual(
            post.author, self.post.author)
        self.assertEqual(
            post.group, self.post.group)
        self.assertEqual(
            post.text, self.post.text)
        self.assertEqual(
            post.pub_date, self.post.pub_date)

    def test_views_have_correct_context(self):
        """ Проверка контекста всех View"""
        all_views = (
            ('posts:index', None, False),
            ('posts:group_list', (self.group.slug,), False),
            ('posts:profile', (self.user.username,), False),
            ('posts:post_detail', (self.post.id,), True)
        )
        for view_name, args, get_cont in all_views:
            with self.subTest(view_name=view_name):
                self.what_is_in_context(view_name, args, get_cont)

    def test_create_and_edit_posts(self):
        """ Проверка Create Post и Edit Post """
        edit_and_create_test = (
            ('posts:post_edit', (self.post.id,)),
            ('posts:post_create', None)
        )
        for rev_name, args in edit_and_create_test:
            with self.subTest(rev_name=rev_name, args=args):
                response = self.authorized_client.get(
                    reverse(rev_name, args=args))
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], PostForm)
                check_form_fields = (
                    ('text', forms.fields.CharField),
                    ('group', forms.fields.ChoiceField)
                )
                for field, field_type in check_form_fields:
                    with self.subTest(field=field):
                        form_field = response.context.get(
                            'form').fields.get(field)
                        self.assertIsInstance(
                            form_field, field_type
                        )

    def test_in_intended_group(self):
        """ Тест пост попал в нужную группу """
        response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.second_group.slug,))
        )
        self.assertEqual(len(response.context.get('page_obj').object_list), 0)
        post = Post.objects.first()
        self.assertTrue(post.group)
        response_to_group = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group.slug,))
        )
        self.assertIn(
            post, response_to_group.context['page_obj'].object_list
        )
