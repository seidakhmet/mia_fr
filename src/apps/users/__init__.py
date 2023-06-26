from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class GroupTypes(TextChoices):
    SIMPLE = ("SIMPLE", _("SIMPLE"))
    MODERATORS = ("MODERATORS", _("MODERATORS"))
    # TODO: добавить больше типов групп, пока не известно какие еще будут
