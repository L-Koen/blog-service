"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os
from dotenv import load_dotenv
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Load environment variables
ENV_FILE = "/app/.env"
load_dotenv(ENV_FILE)


def redirect_to_static_home(request):
    return redirect("/")


urlpatterns = [
    path(os.getenv("ADMIN_URL", "admin/"), admin.site.urls, name="admin"),
    path("blog/", include(("posts.urls", "posts"), namespace="posts")),
    path("", redirect_to_static_home, name="home"),
]
