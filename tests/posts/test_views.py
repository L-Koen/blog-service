import pytest
from django.urls import reverse
from bs4 import BeautifulSoup
from posts.models import Post


@pytest.mark.django_db
class TestLandingView():
    """Test landing page (/.)"""
    def test_status_code(self, client):
        """Test status code of the landing page."""
        print(reverse("landing"))
        response = client.get(reverse('landing'))
        assert response.status_code == 200
        assert "Welcome to Tinkeringalong!" in str(response.content)

    def test_has_blog_link(self, client):
        """Test if there is a link to blog on landing page"""
        response = client.get(reverse('landing'))
        soup = BeautifulSoup(response.content, 'html.parser')
        assert soup.find("a", {"href": reverse('posts:home')}).text == "Blog"


class TestBlogHomePage:
    """Tests for the blog home page."""

    def test_blog_home_loads(self, client, single_post):
        """Ensure the blog page loads properly."""
        url = reverse("posts:home")
        response = client.get(url)

        assert response.status_code == 200
        assert single_post.title in response.content.decode()  # Verify test post appears

    def test_blog_home_shows_latest_posts(self, client, multiple_posts):
        """Ensure multiple recent posts are displayed."""
        url = reverse("posts:home")
        response = client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        post_titles = [h3.text for h3 in soup.find_all("h3")]
        assert "Second Post" in post_titles  # Most recent first
        assert "First Post" in post_titles
