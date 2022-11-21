from django.test import SimpleTestCase
from blog.forms import EmailPostForm, CommentForm
from blog.tests.test_ModelMixinTestCase import ModelMixinTestCase


class TestCommentsForm(ModelMixinTestCase, SimpleTestCase):
    def test_comment_form_valid_data(self):

        self.assertTrue(self.Commentform.is_valid())

    def test_comment_form_invalid_data(self):
        form = CommentForm(
            data={
                "post": self.published_post,
                "name": "First comment",
                "email": "invalid-email",
                "body": "this is comment body",
            }
        )
        self.assertFalse(form.is_valid())

    def test_comment_form_no_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
