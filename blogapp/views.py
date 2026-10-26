
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Blog
from .serializers import BlogSerializer
from functools import wraps
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Blog
from .forms import BlogForm


class BlogListAPIView(generics.ListAPIView):

    serializer_class = BlogSerializer

    permission_classes = [AllowAny]

    queryset = Blog.objects.filter(is_published=True)


class BlogDetailAPIView(generics.RetrieveAPIView):

    serializer_class = BlogSerializer

    permission_classes = [AllowAny]

    lookup_field = "id"

    queryset = Blog.objects.filter(is_published=True)




from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Blog
from .forms import BlogForm


def superuser_required(view_func):
    @wraps(view_func)
    @login_required(login_url="master-login")
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("master-login")
        return view_func(request, *args, **kwargs)
    return wrapper


def master_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("master-blog-list")
        logout(request)

    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("master-blog-list")

        error = "Invalid username/password or superuser access denied."

    return render(
        request,
        "blogapp/dashboard/login.html",
        {"error": error},
    )


@superuser_required
def master_blog_list(request):
    query = request.GET.get("q", "").strip()
    blogs = Blog.objects.all()

    if query:
        blogs = blogs.filter(title__icontains=query)

    blog_items = [
        {
            "blog": blog,
            "form": BlogForm(instance=blog),
        }
        for blog in blogs
    ]

    total = Blog.objects.count()
    published = Blog.objects.filter(is_published=True).count()

    return render(
        request,
        "blogapp/dashboard/blog_list.html",
        {
            "blog_items": blog_items,
            "query": query,
            "create_form": BlogForm(),
            "total_blogs": total,
            "published_blogs": published,
            "draft_blogs": total - published,
        },
    )


@superuser_required
@require_POST
def master_blog_create(request):
    form = BlogForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Blog created successfully.")
    else:
        messages.error(
            request,
            "Could not create the blog. Check all required fields.",
        )

    return redirect("master-blog-list")


@superuser_required
@require_POST
def master_blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    form = BlogForm(request.POST, request.FILES, instance=blog)

    if form.is_valid():
        form.save()
        messages.success(request, "Blog updated successfully.")
    else:
        messages.error(
            request,
            f"Could not update '{blog.title}'. Check the submitted fields.",
        )

    return redirect("master-blog-list")


@superuser_required
@require_POST
def master_blog_delete(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    title = blog.title
    blog.delete()

    messages.success(request, f"'{title}' was deleted.")
    return redirect("master-blog-list")


@superuser_required
@require_POST
def master_logout(request):
    logout(request)
    return redirect("master-login")


