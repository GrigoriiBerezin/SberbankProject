from django.contrib import admin
from django.core.checks import messages
from django.db import models
from django.utils.translation import gettext_lazy as _

import configurations
from .models import Message, City


class MessageListToBeResolvedFilter(admin.SimpleListFilter):
    title = _('to be resolved')
    parameter_name = 'resolve'

    def lookups(self, request, model_admin):
        return (
            ('to resolve', _('To resolve')),
            ('resolved', _('Resolved')),
            ('not marked', _('In progress'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'to resolve':
            return queryset.filter(status__exact=Message.STATUS_CHOICES_DICT["Marked Message"], resolved=False)
        if self.value() == 'resolved':
            return queryset.filter(resolved=True)
        if self.value() == 'not marked':
            return queryset.exclude(status__exact=Message.STATUS_CHOICES_DICT["Marked Message"])


@admin.action(description='Mark messages as resolved')
def make_resolved(model_admin, request, queryset: models.QuerySet):
    limit = configurations.admin["error_show_limit"]
    not_final_messages = queryset.exclude(status__exact=Message.STATUS_CHOICES_DICT["Marked Message"])
    if len(not_final_messages) != 0:
        not_final_ids = [str(field_id[0]) for field_id in not_final_messages.values_list('id')]
        ids_to_show = ', '.join(not_final_ids[:limit]) + '...' if len(not_final_ids) > limit else ', '.join(
            not_final_ids)
        model_admin.message_user(request, f"Messages with ids: ({ids_to_show}) are not in Marked Message status",
                                 level=messages.ERROR)
    else:
        queryset.update(resolved=True)


# Register your models here.
@admin.register(Message)
@admin.display(ordering='-created_at')
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'source', 'status', 'category_type', 'resolved', 'created_at']
    list_filter = (MessageListToBeResolvedFilter,)
    actions = [make_resolved]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
