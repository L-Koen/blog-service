from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from posts import views

app_name = "posts"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="blog"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
