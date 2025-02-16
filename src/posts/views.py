from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.conf import settings
from posts.models import Post

BASE_DIR = settings.BASE_DIR

class HomePageView(ListView):
    """Home view for the blog app."""
    model = Post
    template_name = str(BASE_DIR) + '/posts/templates/posts/blog_home.html'
    context_object_name = "posts"
