import pytest
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from posts.models import Post, Keyword

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
def large_number_posts(db):
    """Returns a larger number of posts, all published."""
    posts = [Post.objects.create(title=f"Post {i}", content="A"*i) for i in range(9)]
    return posts

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

@pytest.fixture
def long_post(db):
    """Create extra long post to test preview"""
    return Post.objects.create(
        title="Very Long Post",
        content="\n".join([f"This is line {i}." for i in range(100)])
    )

@pytest.fixture
def test_image():
    """Creates a temporary in-memory image for testing."""
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Create a red square
    img_io = BytesIO()
    img.save(img_io, format="JPEG")
    img_io.seek(0)

    return SimpleUploadedFile("test_image.jpg", img_io.getvalue(), content_type="image/jpeg")

@pytest.fixture
def test_keyword(db):
    """Creates a sample keyword."""
    return Keyword.objects.create(name="Python")

@pytest.fixture
def test_post_with_keyword(db, test_keyword):
    """Creates a sample post with a keyword."""
    post = Post.objects.create(title="Django & Python", content="Using Python in Django.")
    post.keywords.add(test_keyword)  # Attach the keyword
    return post

@pytest.fixture
def test_posts_filter(db):
    """Creates 2 posts. One with the keywords Django and Python,
    a second with only Python"""
    post1 = Post.objects.create(title="Django & Python", content="Using Python in Django.")
    post2 = Post.objects.create(title="Data Analysis with Python", content="Using Pandas, Numpy, and SciPy.")
    python = Keyword.objects.create(name='Python')
    django = Keyword.objects.create(name='Django')
    post1.keywords.add(python, django)
    post2.keywords.add(python)
    return [post1, post2], [python, django]

@pytest.fixture
def ukulele_post(db):
    """Create test post with Ukulele keyword"""
    post = Post.objects.create(title="Ukulele", content="I like playing the Ukulele")
    ukulele = Keyword.objects.create(name="Ukulele")
    post.keywords.add(ukulele)
    return post