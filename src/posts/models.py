from django.db import models
import markdown
from os import remove
from django.utils.timezone import now
from bs4 import BeautifulSoup

class Keyword(models.Model):
    """Model for keywords (Tags)"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BlogImage(models.Model):
    """Model to store blog post images with optional alt text."""
    image = models.ImageField(upload_to="blog_images")
    alt_text = models.CharField(max_length=255, blank=True)

    def delete(self, *args, **kwargs):
        """Delete the file from storage when the model instance is deleted."""
        file_path = None
        if self.image and self.image.storage.exists(self.image.name):
            file_path = self.image.path
        super().delete(*args, **kwargs)
        if file_path:
            remove(file_path)

    def __str__(self):
        return f"{self.id} - {self.image.name}"


class Post(models.Model):
    """Model representing a blog post."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    keywords = models.ManyToManyField(Keyword, related_name="posts", blank=True)
    published = models.BooleanField(default=True)

    def render_markdown(self):
        """Render markdown. Look for images, to embed their alt-text"""
        # 1) Render post
        rendered_html = markdown.markdown(self.content, extensions=["extra", "codehilite", "toc"])

        # 2) Return if it does not contain images
        if "<img" not in rendered_html:
            return rendered_html

        # 3) For each image, add alt text
        soup = BeautifulSoup(rendered_html, "html.parser")
        for img in soup.find_all("img"):
            image_name = img["src"].split("/")[-1]
            image_obj = BlogImage.objects.filter(image__contains=image_name).first()

            # Only add alt-text if img is found and has text
            if image_obj and image_obj.alt_text:
                img["alt"] = image_obj.alt_text

        # 4) Return updated soup
        return str(soup)

    def preview(self, lines=20):
        post = self.render_markdown()
        return "\n".join(post.split("\n")[:lines])

