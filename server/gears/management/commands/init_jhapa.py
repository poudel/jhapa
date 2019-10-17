from django.core.management import BaseCommand, call_command, CommandError
from django.contrib.sites.models import Site
from django.conf import settings
from gears.models import SiteDetail, User
from links.models import Post


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            raise CommandError("Please don't run this command on production.")

        try:
            site = Site.objects.get(id=1)
        except Site.DoesNotExist:
            raise CommandError("Skip sites.Site update because site 1 doesn't exist.")
        else:
            self.stdout.write("Setting the domain to `localhost` and renaming site to `jhapa`")
            site.domain = "localhost"
            site.name = "jhapa"
            site.save()

            SiteDetail.objects.get_or_create(site=site)

        if User.objects.exists():
            self.stdout.write(
                "Skip createsuperuser because users already present in the database."
            )
        else:
            call_command("createsuperuser")

        if not Post.objects.exists():
            self.stdout.write("Load links.Post.json")
            call_command("loaddata", "links.Post.json")
        else:
            self.stdout.write("Skip links.Post.json because post table not empty")

        self.stdout.write("Load flatpages.json")
        call_command("loaddata", "flatpages.json")
