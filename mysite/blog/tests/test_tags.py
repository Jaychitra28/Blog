from django.test import TestCase
from blog.templatetags import blog_tags
from blog.models import Post, Comment
from blog.tests.test_ModelMixinTestCase import ModelMixinTestCase


class TestTemplateTags(ModelMixinTestCase, TestCase):
    def test_count_tag(self):
        self.assertEqual(blog_tags.total_posts(), 2)

    def test_latest_post_post_tag(self):
        latestpost = blog_tags.show_latest_posts()
        self.assertEquals(latestpost["latest_posts"][0].title, "Two")

    def test_most_commented_post_tag(self):
        most_commented_posts = blog_tags.get_most_commented_posts()
        self.assertEqual(most_commented_posts[0].title, "Two")
