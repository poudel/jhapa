from django.contrib import admin
from gears.models import SiteDetail, User


@admin.register(SiteDetail)
class SiteDetailAdmin(admin.ModelAdmin):
    list_display = ['site']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
