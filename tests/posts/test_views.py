import pytest
from django.urls import reverse
from bs4 import BeautifulSoup
from posts.models import Post, Keyword, BlogImage


@pytest.mark.django_db
class TestLandingView():
    """Test landing page (/.)"""
    def test_status_code(self, client):
        """Test status code of the landing page."""
        response = client.get(reverse('landing'))
        assert response.status_code == 200
        assert "Welcome to Tinkeringalong!" in str(response.content)

    def test_has_blog_link(self, client):
        """Test if there is a link to blog on landing page"""
        response = client.get(reverse('landing'))
        soup = BeautifulSoup(response.content, 'html.parser')
        assert soup.find("a", {"href": reverse('posts:home')}).text == "Blog"


@pytest.mark.django_db
class TestBlogHomePage:
    """Tests for the blog home page."""

    def test_blog_home_loads(self, client, single_post):
        """Ensure the blog page loads properly."""
        url = reverse("posts:home")
        response = client.get(url)

        assert response.status_code == 200
        assert single_post.title in response.content.decode()  # Verify test post appears

    def test_blog_home_shows_latest_posts(self, client, multiple_posts):
        """Ensure multiple recent posts are displayed, latest first."""
        url = reverse("posts:home")
        response = client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        post_titles = [h3.text for h3 in soup.find_all("h3")]
        assert "Second Post" in post_titles  # Most recent first
        assert "First Post" in post_titles
        assert len(response.context["posts"]) == 2
        for i, item in enumerate(response.context["posts"]):
            assert item.id == (2 - i)

    def test_pagination_list(self, client, large_number_posts):
        """Ensure pagination works properly. 5 posts by default"""
        # Setup
        url = reverse("posts:home")

        # Test first 5 posts
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.context["posts"]) == 5

        # Test link to next page
        assert 'href="?page=2"' in response.content.decode()

        # Test second page of results
        response = client.get(f"{url}?page=2")
        assert response.status_code == 200
        assert len(response.context["posts"]) == 4

        # Test link to previous page
        assert 'href="?page=1"' in response.content.decode()

    def test_links_to_item_view(self, client, multiple_posts):
        """ Test that it actually links to the posts"""
        # Setup
        url = reverse("posts:home")
        response = client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Execute
        link_tags = soup.find_all("a", href=True, class_="post-link")
        
        # Verify
        assert len(link_tags) == len(multiple_posts)
        for i, link in enumerate(link_tags):
            expected_url = reverse(
                "posts:post_detail",
                kwargs={"pk": multiple_posts[1-i].id}
            )
            assert link["href"] == expected_url
            assert link.text == multiple_posts[1-i].title
        

@pytest.mark.django_db
class TestKeywordFilterUI:
    """Test that the keyword filter UI elements are present on the blog home page."""

    def test_keyword_filter_dropdown_present(self, client):
        """Ensure a multiple-selection dropdown for keyword filtering is present."""
        response = client.get(reverse("posts:home"))
        soup = BeautifulSoup(response.content, "html.parser")
        select = soup.find("select", {"name": "keywords", "multiple": True})

        assert select is not None, "The keyword multi-select dropdown should exist."

    def test_and_or_selector_present(self, client):
        """Ensure a radio button or dropdown is available to choose AND/OR filtering."""
        response = client.get(reverse("posts:home"))
        soup = BeautifulSoup(response.content, "html.parser")
        and_or_selector = soup.find("select", {"name": "filter_mode"}) or \
                          soup.find("input", {"type": "radio", "name": "filter_mode"})

        assert and_or_selector is not None, "The AND/OR filtering selector should exist."


@pytest.mark.django_db
class TestKeywordFiltering:
    """Test that filtering by keywords works correctly in both AND & OR modes."""

    def test_or_filtering_returns_any_matching_posts(self, client, test_posts_filter):
        """Ensure OR filtering returns posts with at least one matching keyword."""
        # Setup
        posts, keywords = test_posts_filter
        test_post1 = posts[0]
        test_post2 = posts [1]
        python = keywords[0].name
        django = keywords[1].name

        # Execute
        url = reverse("posts:home") + f"?keywords={python},{django}&filter_mode=OR"
        response = client.get(url)

        assert response.status_code == 200
        assert test_post1.title in response.content.decode(), "Post with Django & Python should appear."
        assert test_post2.title in response.content.decode(), "Post with Python should appear."

    def test_and_filtering_returns_only_posts_with_all_keywords(self, client, test_posts_filter):
        """Ensure AND filtering returns only posts that match ALL selected keywords."""
        # Setup
        posts, keywords = test_posts_filter
        test_post1 = posts[0]
        test_post2 = posts [1]
        python = keywords[0].name
        django = keywords[1].name

        # Execute
        url = reverse("posts:home") + f"?keywords={python},{django}&filter_mode=AND"
        response = client.get(url)

        assert response.status_code == 200
        assert test_post1.title in response.content.decode(), "Post with Python & Django should appear."
        assert test_post2.title not in response.content.decode(), "Post with only Python should NOT appear."


@pytest.mark.django_db
class TestTextSearchUI:
    """Test that the full-text search input field is present."""

    def test_text_search_field_present(self, client):
        """Ensure a normal text search input field and submit button exist."""
        response = client.get(reverse("posts:home"))
        soup = BeautifulSoup(response.content, "html.parser")

        text_input = soup.find("input", {"type": "text", "name": "search"})
        submit_button = soup.find("button", {"type": "submit"})

        assert text_input is not None, "Text search input should exist."
        assert submit_button is not None, "Search submit button should exist."


@pytest.mark.django_db
class TestTextSearchFunctionality:
    """Test that full-text search returns correct results."""

    def test_search_finds_matching_posts(self, client, test_posts_filter):
        """Ensure search returns posts with matching content."""
        posts, keywords = test_posts_filter
        test_post1 = posts[0]
        test_post2 = posts [1]
        python = keywords[0].name
        django = keywords[1].name
        url = reverse("posts:home") + "?search=Django"
        response = client.get(url)

        assert response.status_code == 200
        assert test_post1.title in response.content.decode(), "Post with 'Django' should appear."
        assert test_post2.title not in response.content.decode(), "Post without 'Django' should NOT appear."

    def test_search_returns_no_results_for_nonexistent_text(self, client):
        """Ensure search returns no posts if no matches exist."""
        url = reverse("posts:home") + "?search=NonExistentTerm"
        response = client.get(url)

        assert response.status_code == 200
        assert "No posts yet." in response.content.decode(), "Should show empty result message."


@pytest.mark.django_db
class TestItemView:
    """Tests for the individual blog post view."""

    def test_status_code(self, client, single_post):
        """Test that a published post returns a 200 status code."""
        url = reverse("posts:post_detail", args=[single_post.id])
        response = client.get(url)
        assert response.status_code == 200, "Published post should return 200 OK."

    def test_404_for_nonexistent_post(self, client):
        """Test that accessing a non-existent post returns 404."""
        url = reverse("posts:post_detail", args=[99999])  # Assuming no post has this ID
        response = client.get(url)
        assert response.status_code == 404, "Non-existent post should return 404."

    def test_post_content_displayed(self, client, single_post):
        """Test that post title and content appear correctly."""
        url = reverse("posts:post_detail", args=[single_post.id])
        response = client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        assert soup.find("h1", string=single_post.title), "Post title should be displayed."
        assert single_post.content[:50] in response.content.decode(), "Post content should be visible."

    def test_markdown_rendering(self, client, markdown_post):
        """Test that markdown content is correctly rendered to HTML."""
        url = reverse("posts:post_detail", args=[markdown_post.id])
        response = client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        assert soup.find("strong"), "Markdown bold text should be rendered."

    def test_images_are_displayed(self, client, test_image):
        """Test that images in a post are properly displayed."""
        # Setup
        """Creates a test image with alt text."""
        test_im = BlogImage.objects.create(
            image="blog_images/test_image.jpg",
            alt_text="This is a test image"
        )
        """And test post with image"""
        content = f"![Placeholder](/media/{test_im.image})"
        test_post = Post.objects.create(title="Test Post", content=content)

        url = reverse("posts:post_detail", args=[test_post.id])
        response = client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        img_tag = soup.find("img")
        assert img_tag, "An <img> tag should be present in image posts."
        assert "src" in img_tag.attrs, "Image tag should have a source (src) attribute."

        # Cleanup
        file_path = test_im.image.path
        test_im.delete()
        assert not test_im.image.storage.exists(file_path)  # Check that the file is gone

    def test_back_to_blog_link(self, client, single_post):
        """Test that a 'Back to Blog' link is present."""
        url = reverse("posts:post_detail", args=[single_post.id])
        response = client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        back_link = soup.find("a", href=reverse("posts:home"))
        assert back_link, "A 'Back to Blog' link should be present."
