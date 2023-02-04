from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .models import Comment, Group, Post, User
from .forms import CommentForm, PostForm
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
    comments = get_post.comments.all()  # Комментарии к посту
    comment_form = CommentForm()  # Форма коммента
    context = {
        'onepost': onepost,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """ Функция создания поста """
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():  # Валидация формы создания поста
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user.username)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """ Редактирование поста """
    post = get_object_or_404(Post, id=post_id)  # Получения поста
    if post.author != request.user:  # Проверка прав для редактирования
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def create_comment(request, post_id):
    """ Добавление комментария """
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


