from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Post

User = get_user_model()


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='TestUser',
            first_name='Test',
            last_name='User',
            email='testmail@yahoo.com'
        )
        for i in range(1, 15):
            cls.post = Post.object.create(
                text='TestText',
                author=User.objects.get(username='TestUser')
            )

    def setUp(self):
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_five_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)
