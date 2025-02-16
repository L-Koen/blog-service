import pytest
from posts.models import Post

@pytest.mark.django_db
def test_create_post(single_post, single_data):
    post = single_post
    assert post.title == single_data["title"]
    assert single_data["content"] in post.content

def test_post_preview(long_post):
    limit = 15
    post = long_post
    preview = post.preview(limit)
    assert not str(limit) in preview
    assert str(limit-1) in preview