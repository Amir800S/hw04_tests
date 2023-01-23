from django.test import TestCase

from .fixtures import models


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.post = models.post()

    def test_post_have_correct_object_names(self):
        """ Модель Post отображается правильно """
        self.assertEqual(str(self.post), self.post.__str__())

    def test_group_have_correct_object_names(self):
        """ Модель Group отображается правильно """
        self.assertEqual(str(self.group), self.group.__str__())
