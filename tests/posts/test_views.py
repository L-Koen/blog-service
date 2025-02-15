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