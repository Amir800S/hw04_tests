from django.test import Client, TestCase
from django.urls import reverse

from .fixtures import models


class TaskPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.post = models.post()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(TaskPagesTests.user)

    def test_index_show_correct_context(self):
        """ Проверка Index"""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertTrue(response.context['page_obj'].object_list)

    def test_group_list_show_correct_context(self):
        """ Проверка Group List"""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.group, self.group)

    def test_profile_show_correct_context(self):
        """ Проверка Profile"""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username}))
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.author, self.user)

    def test_post_detail_show_correct_context(self):
        """ Проверка Post Detail"""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        first_object = response.context['onepost']
        self.assertEqual(first_object.id, self.post.id )

    def test_post_edit_show_correct_context(self):
        """ Проверка Post Edit"""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}))
        first_object = response.context['post']
        self.assertEqual(first_object.id, self.post.id)

    def test_post_create_show_correct_context(self):
        """ Проверка Post Create"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertTrue(response.context['form'])

    def test_if_post_with_group_on_index(self):
        """ Проверка поста с группой на Index"""
        response = self.authorized_client.get(reverse('posts:index'))
        if self.post.group:
            self.assertIn(self.post, response.context['page_obj'])

    def test_if_post_with_group_on_group_list(self):
        """ Проверка поста с группой на Group List"""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        if self.post.group:
            self.assertIn(self.post, response.context['page_obj'])

    def test_if_post_with_group_on_profile(self):
        """ Проверка поста с группой на Profile"""
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': self.user.username}))
        if self.post.group:
            self.assertIn(self.post, response.context['page_obj'])

    def test_pages_uses_correct_template(self):
        """ Проверка вызываемого шаблона """
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
                'posts/create_post.html',
            reverse('posts:post_create'):
                'posts/create_post.html',
        }
        for reverse_name, template, in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
