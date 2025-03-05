from django.urls import path
from posts import views

app_name = "posts"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail")
]