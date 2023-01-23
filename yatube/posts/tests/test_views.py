from django.test import Client, TestCase
from django.urls import reverse

from .fixtures import models
from ..forms import PostForm
from ..models import Post


class TaskPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.post = models.post()
        cls.second_group = models.second_group()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def what_is_in_context(self, request, get_cont=False):
        if get_cont:
            response = self.authorized_client.get(request)
            self.assertEqual(
                response.context['onepost'].author, self.post.author)
            self.assertEqual(
                response.context['onepost'].group, self.post.group)
            self.assertEqual(
                response.context['onepost'].text, self.post.text)
            self.assertEqual(
                response.context['onepost'].pub_date, self.post.pub_date)

        else:
            response = self.authorized_client.get(request)
            self.assertEqual(
                response.context['page_obj'][0].author, self.post.author)
            self.assertEqual(
                response.context['page_obj'][0].group, self.post.group)
            self.assertEqual(
                response.context['page_obj'][0].text, self.post.text)
            self.assertEqual(
                response.context['page_obj'][0].pub_date, self.post.pub_date)

    def test_index_show_correct_context(self):
        """ Проверка Index"""
        self.what_is_in_context(reverse('posts:index'))

    def test_group_list_show_correct_context(self):
        """ Проверка Group List"""
        self.what_is_in_context(
            reverse('posts:group_list', args=(self.group.slug,)))

    def test_profile_show_correct_context(self):
        """ Проверка Profile"""
        self.what_is_in_context(
            reverse('posts:profile', args=(self.user.username,)))

    def test_post_detail_show_correct_context(self):
        """ Проверка Post Detail"""
        self.what_is_in_context(
            reverse('posts:post_detail', args=(self.post.id,)), True)

    def test_create_and_edit_posts(self):
        """ Проверка Create Post и Edit Post """
        edit_and_create_test = (
            ('posts:post_edit', (self.post.id,)),
            ('posts:post_create', None)
        )
        for rev_name, args in edit_and_create_test:
            with self.subTest(rev_name=rev_name, args=args):
                response = self.authorized_client.get(
                    reverse(rev_name, args=args))
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], PostForm)
        for form_field in response.context['form'].fields:
            with self.subTest(form_field=form_field):
                self.assertTrue(form_field)
                self.assertTrue(form_field)

    def test_in_intended_group(self):
        """ Тест пост попал в нужную группу """
        response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.second_group.slug,)))
        self.assertEqual(len(response.context.get('page_obj').object_list), 0)
        self.assertTrue(Post.objects.latest('id').group)
        response_to_group = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group.slug,)))
        self.assertIn(Post.objects.latest('id'),
                      response_to_group.context['page_obj'].object_list)
