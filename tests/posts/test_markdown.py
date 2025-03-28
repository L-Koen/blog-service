import pytest
from posts.models import Post, BlogImage
from bs4 import BeautifulSoup

@pytest.mark.django_db
def test_markdown_rendering():
    # Setup
    post = Post.objects.create(
        title="Markdown Test",
        content="## Hello World\nThis is a test."
    )

    # Execute
    rendered = post.render_markdown()

    soup = BeautifulSoup(rendered, "lxml")  # or "html.parser"
    header = soup.find("h2", string="Hello World")
    paragraph = soup.find("p", string="This is a test.") 

    # Verify
    assert header is not None
    assert paragraph is not None


@pytest.mark.django_db
def test_markdown_basic_conversion(markdown_post):
    # Setup
    post = markdown_post

    # Execute
    rendered = post.render_markdown()
    soup = BeautifulSoup(rendered, "lxml")  # or "html.parser"
    header = soup.find("h2", string="Heading")
    strong = soup.select_one("p > strong")  # Find <strong> inside a <p>

    # Verify
    assert header is not None
    assert strong is not None and "Bold" in strong.text  



@pytest.mark.django_db
def test_markdown_table_rendering(table_post):
    post = table_post
    rendered = post.render_markdown()

    assert "<table>" in rendered  # Table tag should exist
    assert "<th>Header 1</th>" in rendered  # Header 1 should be in a table header
    assert "<th>Header 2</th>" in rendered  # Header 2 should be in a table header
    assert "<td>Row 1</td>" in rendered  # First row's first column
    assert "<td>Row 2</td>" in rendered  # First row's second column


@pytest.mark.django_db
def test_markdown_code_highlighting(code_post):
    post = code_post
    rendered = post.render_markdown()

    assert '<pre class="codehilite">' in rendered  # Code is highlighted
    assert '<code class="language-python">' in rendered  # Checks correct language class
    assert "print('Hello, world!')" in rendered  # Code is properly converted


@pytest.mark.django_db
def test_markdown_toc_generation(toc_post):
    post = toc_post
    rendered = post.render_markdown()

    assert '<div class="toc">' in rendered  # TOC wrapper should exist
    assert '<a href="#introduction">' in rendered  # TOC should link to Introduction
    assert '<a href="#subheading">' in rendered  # TOC should link to Subheading


@pytest.mark.django_db
def test_render_markdown_adds_alt_text(test_image):
    """Test auto-embedding alt text in markdown images."""
    # Setup
    """Creates a test image with alt text."""
    test_im = BlogImage.objects.create(
        image="blog_images/test_image.jpg",
        alt_text="This is a test image"
    )
    """And test post with image"""
    content = f"![Placeholder](/media/{test_im.image})"
    test_post = Post.objects.create(title="Test Post", content=content)

    # Execute
    rendered = test_post.render_markdown()
    soup = BeautifulSoup(rendered, "html.parser")
    im_tag = soup.find("img")

    # Verify
    assert im_tag is not None
    assert im_tag["alt"] == 'This is a test image'
    assert im_tag.get('src') == f'/blog/media/{test_im.image}'

    # Cleanup
    file_path = test_im.image.path
    test_im.delete()
    assert not test_im.image.storage.exists(file_path)  # Check that the file is gone