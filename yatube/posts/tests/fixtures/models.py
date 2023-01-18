from django.contrib.auth import get_user_model
from ...models import Group, Post

User = get_user_model()


def user():
    return User.objects.create_user(username='TestUser')


def group():
    return Group.objects.create(
        title='TestGroup',
        slug='TestSlug',
        description='TestDesc',
    )


def post():
    return Post.objects.create(
        author=User.objects.get(username='TestUser'),
        text='TestText',
        id=1,
        group=Group.objects.get(slug='TestSlug'),
    )
