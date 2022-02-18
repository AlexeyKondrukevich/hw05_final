from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET, require_http_methods

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


@cache_page(20)
@require_GET
def index(request):
    template = "posts/index.html"
    posts = Post.objects.select_related("author", "group")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, template, context)


@require_GET
def group_posts(request, slug):
    template = "posts/group_list.html"
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related("author")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "page_obj": page_obj,
    }
    return render(request, template, context)


@require_GET
def profile(request, username):
    template = "posts/profile.html"
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related("author", "group")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    following = (
        request.user.is_authenticated
        and Follow.objects.filter(
            author__following__user=request.user
        ).exists()
    )
    context = {"author": author, "page_obj": page_obj, "following": following}
    return render(request, template, context)


@require_GET
def post_detail(request, post_id):
    form = CommentForm()
    template = "posts/post_detail.html"
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related("author")
    context = {"post": post, "form": form, "comments": comments}
    return render(request, template, context)


@login_required
@require_http_methods(["GET", "POST"])
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
@require_http_methods(["GET", "POST"])
def post_create(request):
    template = "posts/create_post.html"
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:profile", post.author)
    context = {"form": form}
    return render(request, template, context)


@login_required
@require_http_methods(["GET", "POST"])
def post_edit(request, post_id):
    template = "posts/create_post.html"
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if request.user != post.author:
        return redirect("posts:post_detail", post.pk)
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post.pk)
    context = {"is_edit": is_edit, "form": form}
    return render(request, template, context)


@login_required
@require_GET
def follow_index(request):
    template = "posts/follow.html"
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, template, context)


@login_required
@require_GET
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(author=author, user=request.user)
    return redirect("posts:profile", username)


@login_required
@require_GET
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    subscription = get_object_or_404(Follow, author=author, user=request.user)
    subscription.delete()
    return redirect("posts:profile", username)
