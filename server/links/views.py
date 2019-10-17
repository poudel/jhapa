from datetime import timedelta
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from links.models import Post
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


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = ReplyForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["request"] = self.request
        return kw

    def get_success_url(self):
        root = self.object.get_root()
        return reverse("post-detail", args=[root.slug])

    def post(self, *args, **kwargs):
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
