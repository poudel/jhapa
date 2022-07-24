from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from gears.constants import DEFAULT_BANNED_DOMAINS


__all__ = ["BaseModel", "SiteDetail"]


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class SiteDetail(BaseModel):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="detail")

    banned_domains = models.TextField(
        _("banned domains"),
        blank=True,
        default=DEFAULT_BANNED_DOMAINS,
        help_text=_(
            "List of domains delimited by a newline (\\n). A list of "
            "tracking/url shortener urls are banned by default."
        ),
    )

    def __str__(self):
        return str(self.site)

    @property
    def banned_domain_list(self):
        return self.banned_domains.split("\n")
