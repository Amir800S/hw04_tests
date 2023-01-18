from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post

User = get_user_model()


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.authorized_client = Client()

    def test_create_post(self):
        form_data = {
            'text': 'TestText',
            'author': 'TestUser',
            'id': 'id',
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        post_count = Post.objects.count()
        self.assertEqual(Post.objects.count(), post_count + 1)

    def test_post_edit(self):
        form_data = {
            'text': 'NewTestText',
            'author': 'TestAuthor',
            'post_id': 'post_id',
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args='post_id'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:post_detail', args='post_id'))
        self.assertTrue(
            Post.objects.filter(
                text='NewTestText',
                author='TestAuthor',
                id='post_id'
            ).exists()
        )
