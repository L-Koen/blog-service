import pytest
from posts.models import Post, BlogImage, Keyword
from django.utils.timezone import now

@pytest.mark.django_db
class TestPostModel():
    def test_create_post(self, single_data):
        """Test creating a single post.
        Do NOT use the single_post pytest fixture, otherwise the before/after
        gets messed up."""
        before = now()
        post = Post.objects.create(**single_data)
        after = now()
        assert post.title == single_data["title"]
        assert single_data["content"] in post.content
        assert before <= post.created_at <= after
        assert before <= post.last_modified <= after

    def test_post_preview(self, long_post):
        """Test if the preview function returns the first #limit lines"""
        limit = 15
        post = long_post
        preview = post.preview(limit)
        assert not str(limit) in preview
        assert str(limit-1) in preview

    def test_post_blog_image(self, test_image):
        blog_image = BlogImage.objects.create(image=test_image)
        # Check that the instance was saved
        assert BlogImage.objects.count() == 1
        assert blog_image.image.name.startswith("blog_images/test_image")  # Check file path
        assert blog_image.image.url == f'/media/{blog_image.image.name}'

        file_path = blog_image.image.path
        print(file_path)

        # Delete image after test
        blog_image.delete()
        assert not blog_image.image.storage.exists(file_path)  # Check that the file is gone

    def test_has_published_status(self, single_data):
        post = Post.objects.create(**single_data)
        # post.published is True by default
        assert hasattr(post, "published")
        assert post.published is True

    def test_unpublish_post(self, single_data):
        single_data["published"] = False
        post = Post.objects.create(**single_data)
        assert post.published is False

    def test_filtering_posts(self, multiple_posts):
        # Setup
        post1, post2 = multiple_posts
        post2.published = False
        post2.save()

        # Execute
        visible_posts = Post.objects.filter(published=True)

        # Verify
        assert visible_posts.count() == 1
        assert visible_posts.first().title == post1.title




@pytest.mark.django_db
class TestKeywordModel():
    """Tests related to the keyword model (and field I'm afraid)"""
    def test_create_keyword(self):
        """Ensure a keyword can be created and retrieved."""
        keyword = Keyword.objects.create(name="Django")
        assert Keyword.objects.count() == 1
        assert keyword.name == "Django"

    def test_post_can_have_keywords(self, test_post_with_keyword, test_keyword):
        """Ensure a post can be linked to a keyword."""
        post = test_post_with_keyword  # Uses the fixture

        assert post.keywords.count() == 1  # Should have 1 keyword
        assert post.keywords.first() == test_keyword  # Should be the expected keyword

    def test_keyword_can_have_multiple_posts(self, test_keyword):
        """Ensure a keyword can be linked to multiple posts."""
        post1 = Post.objects.create(title="Python Post 1", content="Post about Python")
        post2 = Post.objects.create(title="Python Post 2", content="Another post about Python")

        post1.keywords.add(test_keyword)
        post2.keywords.add(test_keyword)

        assert test_keyword.posts.count() == 2  # The keyword should have 2 posts
