from django.test import TestCase

from ..models import Group, Post, User


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
            text='TestTextTestTextTestText',
        )

    def test_post_have_correct_object_names(self):
        self.assertEqual(str(self.post), self.post.__str__())

    def test_group_have_correct_object_names(self):
        self.assertEqual(str(self.group), self.group.__str__())
