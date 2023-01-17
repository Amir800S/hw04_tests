from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .models import Group, Post, User
from .forms import PostForm
from .utils import paginator


def index(request):
    """ Главная страница """
    post_list = Post.objects.select_related('author', 'group').all()
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """ Страница группы """
    group_with_slug = get_object_or_404(Group, slug=slug)
    post_list = group_with_slug.posts.select_related('author').all()
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
        'group': group_with_slug,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """ Страница автора поста """
    user_of_profile = get_object_or_404(User, username=username)
    post_list = user_of_profile.posts.select_related('group').all()
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
        'usermodel': user_of_profile,
        'post_list': post_list  # Отображение числа постов пользователя
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """ Подробное чтение поста """
    get_post = get_object_or_404(Post, id=post_id)
    onepost = get_post
    context = {
        'onepost': onepost,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """ Функция создания поста """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():  # Валидация формы создания поста
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user.username)
        return render(request, 'posts/profile.html', {'form': form})
    form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """ Редактирование поста """
    post = get_object_or_404(Post, id=post_id)  # Получения поста
    if post.author != request.user:  # Проверка прав для редактирования
        return redirect('posts:post_detail', post_id=post_id)
    if request.method == 'POST':
        post_edited = PostForm(instance=post, data=request.POST)
        post_edited.save()
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(instance=post)
    contex = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', contex)
