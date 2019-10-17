# Generated by Django 3.0a1 on 2019-10-17 16:49

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('banned_domains', models.TextField(blank=True, default='1url.com\n7.ly\nadf.ly\nal.ly\nbc.vc\nbit.do\nbit.ly\nbitly.com\nbuzurl.com\ncur.lv\ncutt.us\ndb.tt\ndb.tt\ndoiop.com\nfiloops.info\ngoo.gl\nis.gd\nity.im\nj.mp\nlnkd.in\now.ly\nph.dog\npo.st\nprettylinkpro.com\nq.gs\nqr.ae\nqr.net\nscrnch.me\ns.id\nsptfy.com\nt.co\ntinyarrows.com\ntiny.cc\ntinyurl.com\ntny.im\ntr.im\ntweez.md\ntwitthis.com\nu.bb\nu.to\nv.gd\nvzturl.com\nwp.me\n➡.ws\n✩.ws\nx.co\nyep.it\nyourls.org\nzip.net', help_text='List of domains delimited by a newline (\\n). A list of tracking/url shortener urls are banned by default.', verbose_name='banned domains')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('name', models.CharField(blank=True, help_text='Optional name to display on the profile.', max_length=200, verbose_name='name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Whether the user can log into this admin site.', verbose_name='is a staff')),
                ('is_active', models.BooleanField(default=True, help_text='Can be used for soft-deletion of user.', verbose_name='active')),
                ('avatar', models.ImageField(blank=True, help_text="User's avatar", upload_to='', verbose_name='avatar')),
                ('about', models.CharField(blank=True, help_text='Up to 500 characters, can be styled with markdown.', max_length=500, verbose_name='about')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='sites.Site', verbose_name='site')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]