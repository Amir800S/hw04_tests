from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post
from .fixtures import models


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.second_group = models.second_group()
        cls.post = models.post()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """ Тест отправки формы со страницы Post Create """
        post_count = Post.objects.count()
        form_data = {
            'text': 'TestText',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:profile',
                                     args=(self.user.username,)))

        test_post = Post.objects.latest('id')
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(test_post.text, form_data['text'])
        self.assertEqual(test_post.group.id, form_data['group'])
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit(self):
        """ Тест редактирования формы со страницы Post Edit """
        post_count = Post.objects.count()
        form_data = {
            'text': 'NewTestText',
            'group': self.second_group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=(self.post.id,)),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     args=(self.post.id,)))

        edited_post = Post.objects.latest('id')
        self.assertEqual(edited_post.author, self.post.author)
        self.assertEqual(edited_post.text, form_data['text'])
        self.assertEqual(edited_post.group.pk, form_data['group'])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_for_group = self.client.get(reverse('posts:group_list',
                                                     args=(self.group.slug,)))
        self.assertEqual(response_for_group.status_code, HTTPStatus.OK)
        self.assertNotIn(edited_post, response_for_group.context['page_obj'])
        self.assertEqual(Post.objects.count(), post_count)

    def test_can_not_create_post_guest(self):
        """ Неавторизированный пользователь не может создать пост"""
        form_data = {
            'text': 'Test',
            'group': self.group.pk,
        }
        response = self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
