from django.contrib.auth import get_user_model

from ...models import Group, Post

User = get_user_model()

TEST_RANGE = 5  # Число постов на второй странице Paginator
FIRST_PAGE = 1  # Первая страница Paginator
SECOND_PAGE = 2  # Вторая страница Paginator


def user():
    """ Модель User """
    return User.objects.create_user(username='TestUser')


def second_user():
    """ Модель Second User """
    return User.objects.create_user(username='SecondTestUser')


def group():
    """ Модель Group """
    return Group.objects.create(
        title='TestGroup',
        slug='TestSlug',
        description='TestDesc',
    )


def second_group():
    """ Модель Второй Group для Post Edit """
    return Group.objects.create(
        title='TestGroup2',
        slug='TestSlug2',
        description='TestDesc2',
    )


def post():
    """ Модель Post """
    return Post.objects.create(
        author=User.objects.get(username='TestUser'),
        text='TestTextTestTextTestTextTestText',
        group=Group.objects.get(slug='TestSlug'),
    )


def bulk_post():
    """ Модель Post Bulk Create  """
    return Post.objects.bulk_create([
        Post(text='This is a test',
             author=User.objects.get(username='TestUser'),
             group=Group.objects.get(slug='TestSlug'))
    ])
