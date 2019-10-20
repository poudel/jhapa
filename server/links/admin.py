from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from links.models import Post, Vote, Flag


@admin.register(Post)
class PostAdmin(MPTTModelAdmin):
    list_display = ("__str__", "site", "user", "url")
    list_select_related = ("site", "user")
    list_filter = ["site"]
    readonly_fields = (
        "site",
        "user",
        "parent",
        "title",
        "slug",
        "url",
        "content",
        "status",
        "created_at",
        "modified_at",
    )
    mptt_indent_field = "__str__"
    mptt_level_indent = 10

    # pylint: disable=no-member, protected-access
    mmeta = Post._mptt_meta
    ordering = ["-id", mmeta.tree_id_attr, mmeta.left_attr]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["__str__", "remarks"]
    list_select_related = ["post", "user"]


@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ["__str__", "reason"]
