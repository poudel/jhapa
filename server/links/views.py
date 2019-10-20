from datetime import timedelta

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.utils import timezone
from django.shortcuts import get_object_or_404

from links.models import Post, Flag
from links.forms import PostForm, ReplyForm


class PostListMixin:
    model = Post
    paginate_by = 25

    def get_queryset(self):
        filters = dict(parent__isnull=True, status="Published", site=self.request.site)

        return super().get_queryset().filter(**filters).distinct().order_by("-id")


class IndexView(PostListMixin, ListView):
    pass


class RecentPostList(PostListMixin, ListView):
    def get_queryset(self):
        recent = timezone.now() - timedelta(days=30)
        return super().get_queryset().filter(created_at__gte=recent)


class AskPostList(RecentPostList):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(title__istartswith="Ask:")


class ShowPostList(RecentPostList):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(title__istartswith="Show:")


class PostDetailView(AccessMixin, FormMixin, DetailView):
    model = Post
    form_class = ReplyForm

    # return error response if the user doesn't have permission to access
    raise_exception = True

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["request"] = self.request
        return kw

    def get_success_url(self):
        root = self.object.get_root()
        return reverse("post-detail", args=[root.slug])

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        self.object = self.get_object()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.site = self.request.site
        form.instance.user = self.request.user
        form.instance.parent = self.object
        form.save()
        return super().form_valid(form)


class PostFlagView(LoginRequiredMixin, CreateView):
    model = Flag
    fields = ["reason"]

    def dispatch(self, request, *args, **kwargs):
        post_slug = kwargs['post_slug']
        self.post_item = get_object_or_404(Post, site=request.site, slug=post_slug)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(post_item=self.post_item, **kwargs)

    def form_valid(self, form):
        Flag.flag(self.post_item.id, self.request.user.id, form.instance.reason)
        return HttpResponseRedirect("/")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.site = self.request.site
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", args=[self.object.slug])

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["request"] = self.request
        return kw
