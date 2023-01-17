from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='TestUser',
            first_name='Test',
            last_name='User',
            email='testmail@yahoo.com'
        )

        cls.post = Post.object.create(
            text='TestText',
            author=User.objects.get(username='TestUser')
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_list(self):
        """Страница /group/<slug:slug>/ доступна любому пользователю."""
        response = self.guest_client.get('/group/<slug:slug>/')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        """Страница /profile/<str:username>/ доступна любому пользователю."""
        response = self.guest_client.get('/profile/<str:username>/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        """Страница /posts/<int:post_id>/ доступна любому пользователю."""
        response = self.guest_client.get('/posts/<int:post_id>/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        """Страница /posts/<int:post_id>/edit/ доступна только автору поста."""
        response = self.guest_client.get('/posts/<int:post_id>/edit/', follow=True)
        self.assertRedirects(
            response, '/posts/<int:post_id>/')

    def test_post_create(self):
        """Страница /create/ доступна авторизированному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        """URL использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/<slug:slug>/': 'posts/group_list.html',
            '/profile/<username>/': 'posts/profile.html',
            '/posts/<int:post_id>/': 'posts/post_detail.html',
            '/posts/<int:post_id>/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
