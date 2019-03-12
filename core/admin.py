from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import BookingRecord, Contact, Schedule


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {'fields': (
                'name',
                'email',
                'subject',
                'message',
            )}
        ),
        (
            _('Metadata'),
            {'fields': ('created_at',)}
        ),
    )
    list_display = ('name', 'email', 'subject',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {'fields': (
                'departure',
                'destination',
                'transport_type',
                'date',
                'json_data',
            )}
        ),
        (
            _('Metadata'),
            {'fields': ('created_at',)}
        ),
    )
    list_display = ('departure', 'destination', 'transport_type', 'date',)
    list_filter = ('transport_type', 'created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(BookingRecord)
class BookingRecordAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {'fields': (
                'user',
                'departure',
                'destination',
                'transport_type',
                'date',
                'json_identifier',
            )}
        ),
        (
            _('Metadata'),
            {'fields': ('created_at',)}
        ),
    )
    list_display = ('user', 'departure', 'destination', 'transport_type', 'date',)
    list_filter = ('transport_type', 'created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    raw_id_fields = ('user',)
    search_fields = ('user',)
