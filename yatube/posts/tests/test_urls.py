from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

from .fixtures import models


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.second_user = models.second_user()
        cls.group = models.group()
        cls.post = models.post()

    def setUp(self):
        self.authorized_client = Client()
        self.second_authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.second_authorized_client.force_login(self.second_user)

    def test_urls_with_reverse(self):
        """ Проверка Reverese == URL-адресу"""
        test_urls_with_reverse = (
            ('posts:index', None, '/'),
            ('posts:group_list', (self.group.slug, ),
             f'/group/{self.group.slug}/'),
            ('posts:profile', (self.user.username,),
             f'/profile/{self.user.username}/'),
            ('posts:post_detail', (self.post.id,),
             f'/posts/{self.post.id}/'),
            ('posts:post_edit', (self.post.id,),
             f'/posts/{self.post.id}/edit/'),
            ('posts:post_create', None, '/create/')
        )
        # Проверка Reverse
        for name, args, url in test_urls_with_reverse:
            with self.subTest(name=name, args=args, url=url):
                self.assertEqual(reverse(name, args=args), url)

        # Авторизированный автор
        for name, args, url in test_urls_with_reverse:
            with self.subTest(name=name, args=args, url=url):
                response = self.authorized_client.get(
                    reverse(name, args=args))
                self.assertTrue(response.status_code, HTTPStatus.OK)

        # Авторизированный не автор
        for name, args, url in test_urls_with_reverse:
            with self.subTest(name=name, args=args, url=url):
                response = self.second_authorized_client.get(
                    reverse(name, args=args))
                if name == 'posts:post_edit':
                    self.assertRedirects(response,
                                         reverse('posts:post_detail', args=args))
                else:
                    self.assertTrue(response.status_code, HTTPStatus.OK)

        # Неавторизированный
        for name, args, url in test_urls_with_reverse:
            with self.subTest(name=name):
                response = self.client.get(reverse(name, args=args))
                if name == 'posts:post_edit':
                    self.assertEqual(response.status_code, HTTPStatus.FOUND)
                elif name == 'posts:post_create':
                    self.assertEqual(response.status_code, HTTPStatus.FOUND)
                else:
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """ Reverse использует соответствующий шаблон."""
        templates_check = (
            ('posts:index', None, 'posts/index.html'),
            ('posts:group_list', (self.group.slug,), 'posts/group_list.html'),
            ('posts:profile', (self.user.username,), 'posts/profile.html'),
            ('posts:post_detail', (self.post.id,), 'posts/post_detail.html'),
            ('posts:post_edit', (self.post.id,), 'posts/create_post.html'),
            ('posts:post_create', None, 'posts/create_post.html')
        )
        for rev_name, args, template in templates_check:
            with self.subTest(
                    rev_name=rev_name,
                    args=args,
                    template=template
            ):
                response = self.authorized_client.get(
                    reverse(rev_name, args=args))
                self.assertTemplateUsed(response, template)

    def test_unexisting_page(self):
        """ Проверка несуществующей страницы"""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
