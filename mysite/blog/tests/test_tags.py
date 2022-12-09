from django.test import TestCase
from blog.templatetags import blog_tags
from blog.models import Post, Comment
from blog.tests.test_modelmixintestcase import ModelMixinTestCase


class TestTemplateTags(ModelMixinTestCase, TestCase):
    def test_total_post_tag_returns_total_number_of_posts(self):
        self.assertEqual(blog_tags.total_posts(), 1)

    def test_latest_post_post_tag(self):
        post = Post.objects.create(
            title="latest",
            author=self.user,
            body="Testing Published",
            status="published",
            slug="published",
        )
        self.assertEqual(
            post.title,
            blog_tags.show_latest_posts()["latest_posts"].first().title,
        )

    def test_most_commented_post_tag(self):

        most_commented_post = self.create_commented_posts(
            self.published_post, 10
        )
        self.assertEqual(
            blog_tags.get_most_commented_posts().first().title,
            most_commented_post.title,
        )

    def test_post_without_comments(self):

        post_without_comment = self.create_published_posts(1)
        self.assertTrue(
            post_without_comment not in blog_tags.get_most_commented_posts()
        )
