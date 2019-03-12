from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    """
    Model that represents a contact.
    """
    name = models.CharField(max_length=60)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} sent you a message."


class Schedule(models.Model):
    """
    Model that represents a schedule.
    """
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    transport_type = models.CharField(max_length=20)
    date = models.CharField(max_length=20)

    json_data = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedule")
        ordering = ("-created_at",)

    def __str__(self):
        return "{0} schedule from {1} to {2}.".format(self.transport_type,
                                                     self.departure,
                                                     self.destination)


class BookingRecord(models.Model):
    """
    Model that represents a booking record.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="booking_records")
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    transport_type = models.CharField(max_length=20)
    date = models.CharField(max_length=20)

    json_identifier = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Booking Record")
        verbose_name_plural = _("Booking Records")
        ordering = ("-created_at",)

    def __str__(self):
        return "{0} booked a {1} ticket from {2} to {3}.".format(self.user.get_profile_name(),
                                                                self.transport_type,
                                                                self.departure,
                                                                self.destination)
