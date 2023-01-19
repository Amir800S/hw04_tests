from django.test import TestCase, Client

from .fixtures import models


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.post = models.post()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(TaskURLTests.user)

    def test_index(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_list(self):
        """Страница /group/<slug:slug>/ доступна любому пользователю."""
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        """Страница /profile/<str:username>/ доступна любому пользователю."""
        response = self.guest_client.get(f'/profile/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        """Страница /posts/<int:post_id>/ доступна любому пользователю."""
        response = self.guest_client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        """Страница /posts/<int:post_id>/edit/ доступна только автору поста."""
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/',
                                              follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        """Страница /create/ доступна авторизированному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_unexisting_page(self):
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_urls_uses_correct_template(self):
        """URL использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
