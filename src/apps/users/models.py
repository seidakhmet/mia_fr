from django.contrib.auth import models as django_auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _


from apps.common.mixins import models as mixin_models

from . import GroupTypes


class GroupExtra(models.Model):
    """Дополнительные поля к группе"""

    id: int

    group_id: int
    group: "django_auth_models.Group" = models.OneToOneField(
        django_auth_models.Group, related_name="extra", on_delete=models.CASCADE
    )
    type: str = models.CharField(
        verbose_name=_("Group type"),
        choices=GroupTypes.choices,
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name = _("Group extra data")
        verbose_name_plural = _("Group extra datas")

    def __str__(self) -> str:
        return str(self.group)


class User(mixin_models.TimestampModel, django_auth_models.AbstractUser):
    """Пользователи"""

    id: int
    is_developer: bool = models.BooleanField(verbose_name=_("Is developer"), default=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
