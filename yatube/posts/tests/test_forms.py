from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post
from .fixtures import models

User = get_user_model()


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.post = models.post()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(TaskCreateFormTests.user)

    def test_create_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': 'TestText',
            'author': self.user.username,
            'id': self.post.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), post_count + 1)

    def test_post_edit(self):
        form_data = {
            'text': 'NewTestText',
            'author': self.user.username,
            'id': self.post.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=(self.post.id, )),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     args=(self.post.id, )))
        self.assertTrue(
            Post.objects.filter(
                text='NewTestText',
                author=self.user,
                id=self.post.id,
            ).exists()
        )
