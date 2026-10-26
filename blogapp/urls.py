
from django.urls import path
from . import views

urlpatterns = [
    path("master/login/", views.master_login, name="master-login"),
    path("master/logout/", views.master_logout, name="master-logout"),
    path("master/blogs/", views.master_blog_list, name="master-blog-list"),
    path("master/blogs/create/", views.master_blog_create, name="master-blog-create"),
    path("master/blogs/<uuid:blog_id>/edit/", views.master_blog_edit, name="master-blog-edit"),
    path("master/blogs/<uuid:blog_id>/delete/", views.master_blog_delete, name="master-blog-delete"),
]
