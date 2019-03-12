from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    Model that represents a user.
    """
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("User's name"), blank=True, max_length=255)
    picture = models.ImageField(_('Profile picture'),
                                upload_to='profile_pics/',
                                null=True,
                                blank=True)

    def __str__(self):
        return self.username

    def get_profile_name(self):
        if self.name:
            return self.name

        return self.username

    def get_profile_picture(self):
        default_picture = settings.STATIC_URL + 'img/ditto.jpg'
        if self.picture:
            return self.picture.url
        else:
            return default_picture
