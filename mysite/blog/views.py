from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, FormView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect


class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 3
    context_object_name = "posts"
    template_name = "blog/post/list.html"


def paginate(queryset, page, per_page):
    paginator = Paginator(queryset, per_page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return posts


def get(self, request):
    posts = self.paginate(Post.published.all(), request.GET.get("page"), 3)
    return render(
        request,
        self.template_name,
        {"posts": posts, "page": request.GET.get("paginate_by", 3)},
    )


def add_comment(comment_form, post):
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.save()
        return comment


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comment_form = CommentForm(data=request.POST or None)
    comments = add_comment(comment_form, post)
    comment_form = CommentForm()
    redirect(reverse("blog:post_detail", args=[year, month, day, post.slug]))
    messages.success(request, message="Comment added successfully")

    comments = Comment.activated.filter(post=post)
    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


class PostShareView(SuccessMessageMixin, FormView):
    form_class = EmailPostForm
    template_name = "blog/post/share.html"
    success_url = reverse_lazy("blog:post_list")
    success_message = "mail sent"

    def setup(self, request, post_id, *args, **kwargs):
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
        self.request = request
        self.args = args

        post = get_object_or_404(Post, id=post_id, status="published")
        self.kwargs = {"post": post}

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status="published")
        return render(
            request,
            self.template_name,
            {"post": post, "form": EmailPostForm},
        )

    def form_valid(self, form):
        self.send_mail(form.cleaned_data)
        return super(PostShareView, self).form_valid(form)

    def send_mail(self, valid_data):
        post = self.kwargs["post"]
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        send_mail(
            message=f"Read {post.title} at { post_url }\n\n"
            f"{valid_data['from_name']}'s message: {valid_data['share_message']}",
            from_email=valid_data["from_email"],
            subject=f"{valid_data['from_name']} recommends you read {post.title}",
            recipient_list=[valid_data["to_email"]],
        )
