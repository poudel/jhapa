from urllib.parse import urlparse

import bleach

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from gears.models import BaseModel, User
from gears.utils import get_random_string


__all__ = ["Post", "Vote", "Flag"]


class Post(MPTTModel, BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("submitter"),
    )

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="posts", verbose_name=_("site")
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("parent post"),
    )

    title = models.CharField(_("title"), max_length=300, blank=True)
    slug = models.SlugField(_("slug"), unique=False, editable=False)
    url = models.URLField(_("url"), max_length=300, blank=True)
    content = models.TextField(_("content"), blank=True)

    STATUS_CHOICES = [("Published", "Published")]
    status = models.CharField(
        _("status"), max_length=30, choices=STATUS_CHOICES, db_index=True, default="Published"
    )

    class Meta:
        unique_together = [("site", "slug")]
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title or f"{self.content[:40]}"

    def make_slug(self):
        source = slugify(self.title[:30] or self.content[:30])
        if source:
            return f"{source}-" + get_random_string(4)
        return get_random_string(11)

    def set_unique_slug(self):
        if not self.slug:
            slug = self.make_slug()

            while Post.objects.filter(slug=slug, site_id=self.site_id).exists():
                slug = self.make_slug()
            self.slug = slug

    def save(self, *args, **kwargs):
        self.set_unique_slug()
        self.title = bleach.clean(self.title, tags=[])
        self.content = bleach.clean(self.content, tags=[])

        super().save(*args, **kwargs)

        Vote.upvote(self.id, self.user_id)

    @property
    def domain(self):
        if self.url:
            return urlparse(self.url).netloc.split("www.")[-1]


class Vote(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("post"))

    # todo: make this nullable and add a sentinel user ? because we
    # want to retain the votes even if user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))

    VOTE_TYPES = [("upvote", "upvote"), ("downvote", "downvote")]
    vote_type = models.CharField(_("vote type"), max_length=20, choices=VOTE_TYPES)
    remarks = models.CharField(_("remarks"), max_length=250, blank=True)

    class Meta:
        unique_together = [("post", "user")]

    def __str__(self):
        return f"{self.post} -> {self.user} -> {self.get_vote_type_display()}"

    @classmethod
    def vote(cls, post_id, user_id, vote_type, remarks):
        cls.objects.get_or_create(
            post_id=post_id, user_id=user_id, defaults={"vote_type": vote_type, "remarks": remarks}
        )

    @classmethod
    def upvote(cls, post_id, user_id, remarks=""):
        cls.vote(post_id, user_id, "upvote", remarks)

    @classmethod
    def downvote(cls, post_id, user_id, remarks=""):
        cls.vote(post_id, user_id, "downvote", remarks)


class Flag(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("post"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))

    FLAG_REASONS = [("spam", "spam"), ("off_topic", "off topic")]

    reason = models.CharField(_("reason"), max_length=20, choices=FLAG_REASONS)

    class Meta:
        unique_together = [("post", "user")]

    def __str__(self):
        return f"{self.post} -> {self.user}"

    @classmethod
    def flag(cls, post_id, user_id, reason):
        return cls.objects.update_or_create(post_id=post_id, user_id=user_id, reason=reason)

    @classmethod
    def flag_spam(cls, post_id, user_id):
        return cls.flag(post_id, user_id, "spam")

    @classmethod
    def flag_off_topic(cls, post_id, user_id):
        return cls.flag(post_id, user_id, "off_topic")
