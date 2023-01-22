from django.test import Client, TestCase
from django.urls import reverse

from .fixtures import models
from ..forms import PostForm


class TaskPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.post = models.post()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_show_correct_context(self):
        """ Проверка Index"""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertTrue(response.context['page_obj'].object_list)

    def test_group_list_show_correct_context(self):
        """ Проверка Group List"""
        response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group.slug,)))
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.group, self.group)

    def test_profile_show_correct_context(self):
        """ Проверка Profile"""
        response = self.authorized_client.get(
            reverse('posts:profile', args=(self.user.username,)))
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.author, self.user)

    def test_post_detail_show_correct_context(self):
        """ Проверка Post Detail"""
        response = self.authorized_client.get(
            reverse('posts:post_detail', args=(self.post.id,)))
        first_object = response.context['onepost']
        self.assertEqual(first_object.id, self.post.id)

    # def test_post_edit_show_correct_context(self):
    #     """ Проверка Post Edit"""
    #     response = self.authorized_client.get(
    #         reverse('posts:post_edit', args=(self.post.id, )))
    #     first_object = response.context['post']
    #     self.assertEqual(first_object.id, self.post.id)
    #
    # def test_post_create_show_correct_context(self):
    #     """ Проверка Post Create"""
    #     response = self.authorized_client.get(reverse('posts:post_create'))
    #     self.assertTrue(response.context['form'])

    def test_create_and_edit_posts(self):
        """ Проверка Create Post и Edit Post """
        edit_and_create_test = (
            ('posts:post_edit', (self.post.id,)),
            ('posts:post_create', None)
        )
        for rev_name, args in edit_and_create_test:
            with self.subTest(rev_name=rev_name, args=args):
                response = self.authorized_client.get(reverse(rev_name, args=args))
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], PostForm)
            with self.subTest():
                self.assertEqual(response.context['form'].text, 'TestText')
                self.assertEqual(response.context['form'].group, 'TestSlug')

    # def test_if_post_with_group_on_index(self):
    #     """ Проверка поста с группой на Index"""
    #     response = self.authorized_client.get(reverse('posts:index'))
    #     if self.post.group:
    #         self.assertIn(self.post, response.context['page_obj'])
    #
    # def test_if_post_with_group_on_group_list(self):
    #     """ Проверка поста с группой на Group List"""
    #     response = self.authorized_client.get(
    #         reverse('posts:group_list', args=(self.group.slug,)))
    #     if self.post.group:
    #         self.assertIn(self.post, response.context['page_obj'])
    #
    # def test_if_post_with_group_on_profile(self):
    #     """ Проверка поста с группой на Profile"""
    #     response = self.authorized_client.get(
    #         reverse('posts:profile',
    #                 args=(self.user.username,)))
    #     if self.post.group:
    #         self.assertIn(self.post, response.context['page_obj'])

    # def func_for_test_context(self, request, bool=False):
    #     if bool == True:
    #         pass
