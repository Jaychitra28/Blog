from django.test import TestCase
from blog.models import Post
from blog.tests.test_modelmixintestcase import ModelMixinTestCase


class TestPublishedManager(ModelMixinTestCase, TestCase):
    def test_published_manager_should_not_have_draft_post(self):
        self.assertTrue(self.draft_post not in Post.published.all())
