from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.mixins import models as mixin_models
from django.contrib.auth import get_user_model

User = get_user_model()


class FaceRecognitionRequest(mixin_models.UUIDModel, mixin_models.TimestampModel):
    """Запросы на распознавание лиц"""

    id: int

    created_by_id: int
    created_by: User = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Created by")
    )

    def __str__(self):
        return "{0}".format(self.uuid)

    class Meta:
        verbose_name = _("Face recognition request")
        verbose_name_plural = _("Face recognition requests")


class FaceRecognitionOriginalImage(mixin_models.TimestampModel):
    """Оригинальные изображения запросов на распознавание лиц"""

    id: int

    request_id: int
    request: FaceRecognitionRequest = models.ForeignKey(
        FaceRecognitionRequest,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Face recognition request"),
    )

    image = models.ImageField(upload_to="original/%Y/%m/%d/")
