from blog.tests.test_modelmixintestcase import ModelMixinTestCase
from django.test import TestCase
from django.urls import resolve, reverse


class TestModelMethods(ModelMixinTestCase, TestCase):
    def test_absolute_url_in_model(self):
        self.assertEqual(
            reverse(
                "blog:post_detail",
                args=[
                    self.published_post.publish.year,
                    self.published_post.publish.month,
                    self.published_post.publish.day,
                    self.published_post.slug,
                ],
            ),
            self.published_post.get_absolute_url(),
        )
