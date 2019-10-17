from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from links.models import Post


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
        "upvotes",
        "downvotes",
    )
    mptt_indent_field = "__str__"
    mptt_level_indent = 10

    # pylint: disable=no-member, protected-access
    mmeta = Post._mptt_meta
    ordering = ["-id", mmeta.tree_id_attr, mmeta.left_attr]
