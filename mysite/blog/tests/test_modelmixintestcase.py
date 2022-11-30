from django.test import TestCase, Client
from blog.models import Post
from django.contrib.auth.models import User


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="jaya",
            password="1234",
        )

        self.draft_post = Post.objects.create(
            title="Draft",
            author=self.user,
            body="Testing Draft",
            status="draft",
        )
        self.published_post = Post.objects.create(
            title="Published",
            author=self.user,
            body="Testing Published",
            status="published",
            slug="published",
        )

    def create_published_posts(self, count):
        posts = []
        for _ in range(count):
            post = Post.objects.create(
                title="Published2",
                author=self.user,
                body="Testing Published2",
                status="published",
                slug="published2",
            )
            posts.append(post)
        return posts
