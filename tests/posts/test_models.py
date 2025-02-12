import pytest
from posts.models import Post

@pytest.mark.django_db
def test_create_post():
    post = Post.objects.create(
        title="My First Post",
        content="This is a **Markdown** post!"
    )
    assert post.title == "My First Post"
    assert "Markdown" in post.content