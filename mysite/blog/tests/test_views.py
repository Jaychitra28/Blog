from django.test import TestCase
from django.urls import reverse
from blog.models import Post
from blog.tests.test_modelmixintestcase import ModelMixinTestCase


class TestListView(ModelMixinTestCase, TestCase):
    def test_post_list_GET(self):
        response = self.client.get(reverse("blog:post_list"))

        self.assertTemplateUsed(response, "blog/post/list.html")

    def test_pagination_returns_404_if_page_out_of_range(self):
        response = self.client.get(
            reverse("blog:post_list"),
            {"page": 999, "posts": self.create_published_posts(4)},
        )
        self.assertEquals(response.status_code, 404)

    def test_pagination_returns_404_if_String_is_passed_in_page(self):
        response = self.client.get(
            reverse("blog:post_list"),
            {"page": "test", "posts": self.create_published_posts(4)},
        )
        self.assertEquals(response.status_code, 404)


class TestDetailView(ModelMixinTestCase, TestCase):
    def test_post_detail_template_used(self):
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[
                    self.published_post.publish.year,
                    self.published_post.publish.month,
                    self.published_post.publish.day,
                    self.published_post.slug,
                ],
            )
        )

        self.assertTemplateUsed(response, "blog/post/detail.html")

    def test_post_detail_should_return_404_for_invalid_post(self):

        incorrect_year = "2093"
        incorrect_month = "12"
        incorrect_day = "7"
        incorrect_slug = "incorrect_slug"

        incorrect_post_detail_url = reverse(
            "blog:post_detail",
            args=[
                incorrect_year,
                incorrect_month,
                incorrect_day,
                incorrect_slug,
            ],
        )
        response = self.client.get(incorrect_post_detail_url)

        self.assertEqual(404, response.status_code)
