from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, FormView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from taggit.models import Tag


class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 3
    context_object_name = "posts"
    template_name = "blog/post/list.html"


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")

    comment_form = CommentForm(data=request.POST or None)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(request, message="Comment added successfully")
        return redirect(
            "blog:post_detail",
            post.publish.year,
            post.publish.month,
            post.publish.day,
            post.slug,
        )

    return render(
        request,
        "blog/post/detail.html",
        {
            "comment_form": comment_form,
        },
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comment_form": CommentForm,
            "similar_posts": post.get_top_four_similar_posts(),
        },
    )


class PostListByTagview(ListView):
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

    def dispatch(self, request, *args, **kwargs):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get("tag_slug"))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.published.filter(tags__in=[self.tag])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["tag"] = self.tag
        return data


class PostShareView(SuccessMessageMixin, FormView):
    form_class = EmailPostForm
    template_name = "blog/post/share.html"
    success_url = reverse_lazy("blog:post_list")
    success_message = "Mail send Successfully"

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(
            Post, id=self.kwargs.get("post_id")
        )
        return super().dispatch(request, args, kwargs)

    def form_valid(self, form):
        self.send_mail(form.cleaned_data)
        return super(PostShareView, self).form_valid(form)

    def send_mail(self, valid_data):
        post_url = self.request.build_absolute_uri(
            self.post_object.get_absolute_url()
        )
        send_mail(
            message=f"Read {self.post_object.title} at { post_url }\n\n"
            f"{valid_data['from_name']}'s message: {valid_data['share_message']}",
            from_email=valid_data["from_email"],
            subject=f"{valid_data['from_name']} recommends you read {self.post_object.title}",
            recipient_list=[valid_data["to_email"]],
        )
