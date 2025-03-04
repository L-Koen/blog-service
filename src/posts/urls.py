from django.urls import path
from posts.views import HomePageView, PostDetailView


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post_detail")
]