from django.db import models
import markdown


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def render_markdown(self):
        return markdown.markdown(self.content, extensions=["extra", "codehilite", "toc"])