from django.core.management import BaseCommand, call_command
from django.contrib.sites.models import Site
from gears.models import SiteDetail


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        site_id = input("Give us the site ID [1]: ")
        site_id = site_id or 1

        site = Site.objects.get(id=site_id)
        domain = input("Domain [{}]: ".format(site.domain))
        site.domain = domain or site.domain

        name = input("Name [{}]: ".format(site.name))
        site.name = name or site.name

        site.save()

        SiteDetail.objects.get_or_create(site=site)

        call_command("createsuperuser")
