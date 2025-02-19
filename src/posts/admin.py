from django.contrib import admin
from posts.models import Post, Keyword
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    filter_horizontal = ("keywords",)  # Enables a multi-select UI for keywords

admin.site.register(Keyword)