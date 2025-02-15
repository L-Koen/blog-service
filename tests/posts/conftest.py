import pytest
from posts.models import Post

@pytest.fixture
def single_data():
    return {"title":"Test Post", "content":"This is a test post."}

@pytest.fixture
def single_post(db, single_data): # db is the fixture from django conftest.py
    """Creates a single test post (auto rolled back after test)."""
    return Post.objects.create(title=single_data["title"], content=single_data["content"])

@pytest.fixture
def multiple_posts(db):
    """Creates multiple test posts for pagination and ordering tests."""
    return [
        Post.objects.create(title="First Post", content="First"),
        Post.objects.create(title="Second Post", content="Second"),
    ]

@pytest.fixture
def markdown_post(db):
    """Creates a test post with Markdown formatting."""
    return Post.objects.create(
        title="Markdown Test",
        content="## Heading\n**Bold** text",
    )

@pytest.fixture
def table_post(db):
    """Creates a test post with a Table using Markdown formatting."""
    return Post.objects.create(
        title="Table Test",
        content="| Header 1 | Header 2 |\n|----------|----------|\n| Row 1    | Row 2    |"
    )

@pytest.fixture
def code_post(db):
    """Creates a test post with some Python code."""
    return Post.objects.create(
        title="Code Test",
        content="```python\nprint('Hello, world!')\n```"
    )

@pytest.fixture
def toc_post(db):
    """Creates a post with a TOC"""
    return Post.objects.create(
        title="TOC Test",
        content="""# Heading 1\n## introduction\n### subheading\n[TOC]"""
    )