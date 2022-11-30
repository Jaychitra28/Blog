from django.test import SimpleTestCase
from django.urls import resolve, reverse
from blog.tests.test_modelmixintestcase import ModelMixinTestCase
from blog.views import PostListView, post_detail


class TestUrls(ModelMixinTestCase, SimpleTestCase):
    def test_post_list_url_is_resolved(self):
        self.assertEquals(
            resolve(reverse("blog:post_list")).func.view_class, PostListView
        )

    def test_post_detail_url_is_resolved(self):
        self.assertEquals(
            resolve(
                reverse(
                    "blog:post_detail",
                    args=[
                        self.published_post.publish.year,
                        self.published_post.publish.month,
                        self.published_post.publish.day,
                        self.published_post.slug,
                    ],
                )
            ).func,
            post_detail,
        )
