from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='TestGroup',
            slug='TestSlug',
            description='TestDesc',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='TestText',
        )

    def test_models_have_correct_object_names(self):
        check_str = Post()
        self.assertEqual(str(check_str), check_str.__str__())

    def test_group(self):
        check_group = Group()
        self.assertEqual(str(check_group), check_group.__str__())

