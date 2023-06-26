import uuid as _uuid
import datetime
from django.db import models
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _


class TimestampModel(models.Model):
    created_at: "datetime.datetime" = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_("Created time")
    )
    changed_at: "datetime.datetime" = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name=_("Last change time")
    )

    class Meta:
        abstract = True

    @property
    def created_at_pretty(self) -> str:
        return localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")

    created_at_pretty.fget.short_description = _("Created time")

    @property
    def updated_at_pretty(self) -> str:
        return localtime(self.changed_at).strftime("%d.%m.%Y %H:%M:%S")

    updated_at_pretty.fget.short_description = _("Last change time")


class FullNameModel(models.Model):
    first_name = models.CharField(max_length=255, null=False, verbose_name=_("First name"))
    last_name = models.CharField(max_length=255, null=False, verbose_name=_("Last name"))
    middle_name = models.CharField(max_length=255, null=True, verbose_name=_("Middle name"))

    @property
    def full_name(self) -> str:
        return " ".join([name for name in (self.last_name, self.first_name, self.middle_name) if name])

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    uuid: _uuid.UUID = models.UUIDField(_("UUID identification"), default=_uuid.uuid4, unique=True, editable=False)

    class Meta:
        abstract = True
