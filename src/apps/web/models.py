from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    """
    Эта модель смотрит в базу данных системы распознания.
    Не забываем использовать using. Например: queryset = Person.objects.using("fr_db").all()
    Там очень много данных, не пытайтесь вывести её в админку. Web-приложение сдохнет 🤪
    """

    id: int
    iin: str = models.CharField(db_column="gr_code", max_length=255, blank=True, null=True, verbose_name=_("IIN"))
    id_number: str = models.CharField(
        db_column="ud_code", max_length=255, blank=True, null=True, verbose_name=_("ID number")
    )
    first_name: str = models.CharField(
        db_column="firstname", max_length=255, blank=True, null=True, verbose_name=_("First name")
    )
    middle_name: str = models.CharField(
        db_column="secondname", max_length=255, blank=True, null=True, verbose_name=_("Middle name")
    )
    last_name: str = models.CharField(
        db_column="lastname", max_length=255, blank=True, null=True, verbose_name=_("Last name")
    )

    class Meta:
        db_table = "unique_ud_gr_cache"
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
