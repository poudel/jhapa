from django_registration.forms import RegistrationForm

from gears.models.auth import User


class UserRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
