from django.db import models
import markdown
from os import remove
from django.utils.timezone import now
from bs4 import BeautifulSoup, Tag
from bs4.element import AttributeValueList
from typing import cast, List, Union

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
        """Render markdown. Look for images, to embed their alt-text and 
        give them a CSS class for styling."""
        # 1) Render post
        rendered_html = markdown.markdown(self.content, extensions=["extra", "codehilite", "toc"])

        # 2) Return if it does not contain images
        if "<img" not in rendered_html:
            return rendered_html

        # 3) For each image, add alt text
        soup = BeautifulSoup(rendered_html, "html.parser")
        for img in soup.find_all("img"):
            if isinstance(img, Tag) and img.has_attr("src"):
                src = str(img["src"])
                image_name = src.split("/")[-1]
                image_obj = BlogImage.objects.filter(image__contains=image_name).first()

                # Only add alt-text if img is found and has text
                if image_obj and image_obj.alt_text:
                    img["alt"] = image_obj.alt_text
            
                # Also give it a class:
                current_class: Union[str, list[str], None] = img.get("class")  # Explicitly typed
                if isinstance(current_class, list):
                    img["class"] = cast(AttributeValueList, current_class + ["post-image",])
                else:
                    img["class"] = cast(AttributeValueList, ["post-image"])

        # 4) Return updated soup
        return str(soup)

    def preview(self, lines=10):
        """Return short preview of post, excluding images
        Then rebuild the preview to close of tags just in case."""
        post_html = self.render_markdown()
        soup = BeautifulSoup(post_html, "html.parser")

        for img in soup.find_all("img"):
            if isinstance(img, Tag):
                alt_raw = img.get("alt")
                alt_text = alt_raw.strip() if isinstance(alt_raw, str) else ""
                if alt_text:
                    # Replace <img> with its alt text wrapped in <em> for visibility
                    img.replace_with(soup.new_tag("em", string=f"[Image: {alt_text}]"))
                else:
                    img.decompose()  # No alt text = remove it completely

        clean_html = str(soup)

        truncated = "\n".join(clean_html.splitlines()[:lines])
        # Re-parse to auto-close unclosed tags
        soup = BeautifulSoup(truncated, "html.parser")
        return str(soup)
