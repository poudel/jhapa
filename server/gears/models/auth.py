import bleach
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from gears.models.base import BaseModel


__all__ = ["User"]


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
    )
    name = models.CharField(
        _("name"),
        max_length=200,
        blank=True,
        help_text=_("Optional name to display on the profile."),
    )
    email = models.EmailField(_("email address"), blank=True, null=True, unique=True)
    is_staff = models.BooleanField(
        _("is a staff"),
        default=False,
        help_text=_("Whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Can be used for soft-deletion of user.")
    )

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="users", verbose_name=_("site"), null=True
    )

    avatar = models.ImageField(_("avatar"), blank=True, help_text=_("User's avatar"))

    about = models.CharField(
        _("about"),
        max_length=500,
        help_text=_("Up to 500 characters, can be styled with markdown."),
        blank=True,
    )

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.about = bleach.clean(self.about, tags=[])
        super().save(*args, **kwargs)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
