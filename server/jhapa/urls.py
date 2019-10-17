from django.contrib import admin
from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView
from gears.forms import UserRegistrationForm


urlpatterns = [
    path(
        'accounts/register/',
        RegistrationView.as_view(form_class=UserRegistrationForm, success_url='/'),
        name='django_registration_register',
    ),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('links.urls')),
]
