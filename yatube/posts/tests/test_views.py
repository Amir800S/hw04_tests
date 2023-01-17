from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .test_models import PostModelTest

User = get_user_model()


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostModelTest()

    def setUp(self):
        self.guest_client = Client()  # Неавторизированный клиент
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_show_correct_context(self):
        """ Проверка paginator Index"""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.context['page_obj'].count(), 10)

    def test_group_list_show_correct_context(self):
        """ Проверка paginator Group List"""
        response = self.authorized_client.get(reverse('posts:group_list'))
        self.assertEqual(response.context['page_obj'].count(), 10)
        first_object = response.context['page_obj'][0]
        group_post_author = first_object.slug
        self.assertEqual(group_post_author, 'TestSlug')

    def test_profile_show_correct_context(self):
        """ Проверка paginator Profile"""
        response = self.authorized_client.get(reverse('posts:profile'))
        self.assertEqual(response.context['page_obj'].count(), 10)
        first_object = response.context['page_obj'][0]
        profile = first_object.author
        self.assertEqual(profile, 'TestUser')

    def test_post_detail_show_correct_context(self):
        """ Проверка Post Detail"""
        response = self.authorized_client.get(reverse('posts:post_detail'))
        first_object = response.context['onepost'][0]
        post_id = first_object.id
        self.assertEqual(post_id, 1)

    def test_post_edit_show_correct_context(self):
        """ Проверка Post Edit"""
        response = self.authorized_client.get(reverse('posts:post_edit'))
        first_object = response.context['form'][0]
        post_id = first_object.id
        self.assertEqual(post_id, 1)

    def test_post_create_show_correct_context(self):
        """ Проверка Post Create"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form = response.context['form']
        self.assertTrue(form)

    def test_pages_uses_correct_template(self):
        """ Проверка вызываемого шаблона """
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list'): 'posts/group_list.html',
            reverse('posts:profile'): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'id': 'post_id'}):
                'posts/posts_detail.html',
            reverse('posts:post_edit', kwargs={'id': 'post_id'}):
                'posts/create_post.html',
            reverse('posts:post_create'):
                'posts/create_post.html',
        }
        for reverse_name, template, in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
