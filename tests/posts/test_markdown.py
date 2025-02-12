import pytest
from posts.models import Post
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
def test_markdown_basic_conversion():
    # Setup
    post = Post.objects.create(title="Markdown Test", content="## Heading\n**Bold** text")

    # Execute
    rendered = post.render_markdown()
    soup = BeautifulSoup(rendered, "lxml")  # or "html.parser"
    header = soup.find("h2", string="Heading")
    strong = soup.select_one("p > strong")  # Find <strong> inside a <p>

    # Verify
    assert header is not None
    assert strong is not None and "Bold" in strong.text  



@pytest.mark.django_db
def test_markdown_table_rendering():
    post = Post.objects.create(
        title="Table Test",
        content="| Header 1 | Header 2 |\n|----------|----------|\n| Row 1    | Row 2    |"
    )
    rendered = post.render_markdown()

    assert "<table>" in rendered  # Table tag should exist
    assert "<th>Header 1</th>" in rendered  # Header 1 should be in a table header
    assert "<th>Header 2</th>" in rendered  # Header 2 should be in a table header
    assert "<td>Row 1</td>" in rendered  # First row's first column
    assert "<td>Row 2</td>" in rendered  # First row's second column


@pytest.mark.django_db
def test_markdown_code_highlighting():
    post = Post.objects.create(
        title="Code Test",
        content="```python\nprint('Hello, world!')\n```"
    )
    rendered = post.render_markdown()

    assert '<pre class="codehilite">' in rendered  # Code is highlighted
    assert '<code class="language-python">' in rendered  # Checks correct language class
    assert "print('Hello, world!')" in rendered  # Code is properly converted


@pytest.mark.django_db
def test_markdown_toc_generation():
    post = Post.objects.create(
        title="TOC Test",
        content="# Introduction\n## Subheading\n[TOC]"
    )
    rendered = post.render_markdown()

    assert '<div class="toc">' in rendered  # TOC wrapper should exist
    assert '<a href="#introduction">' in rendered  # TOC should link to Introduction
    assert '<a href="#subheading">' in rendered  # TOC should link to Subheading
