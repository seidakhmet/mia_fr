from django.contrib.postgres.fields import ArrayField
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


class OriginalImage(mixin_models.UUIDModel, mixin_models.TimestampModel):
    """Оригинальные изображения запросов на распознавание лиц"""

    id: int

    request_id: int
    request: FaceRecognitionRequest = models.ForeignKey(
        FaceRecognitionRequest,
        on_delete=models.CASCADE,
        related_name="images",
        null=False,
        blank=False,
        verbose_name=_("Face recognition request"),
    )

    image = models.ImageField(upload_to="originals/%Y/%m/%d/", verbose_name=_("Image"))
    unique_id: str = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Identity of result"))
    results_path: str = models.CharField(
        max_length=1000, null=False, blank=False, verbose_name=_("Path to results folder")
    )
    face_ids: list = ArrayField(
        models.IntegerField(blank=True), default=list[0], blank=True, verbose_name=_("Face identities")
    )

    def __str__(self):
        return "{0}".format(self.uuid)

    class Meta:
        verbose_name = _("Original image")
        verbose_name_plural = _("Original images")


class DetectedFace(mixin_models.UUIDModel, mixin_models.TimestampModel):
    """Обнаруженные лица"""

    id: int

    original_image_id: int
    original_image: OriginalImage = models.ForeignKey(
        OriginalImage,
        on_delete=models.CASCADE,
        related_name="faces",
        null=False,
        blank=False,
        verbose_name=_("Original image"),
    )
    image = models.ImageField(upload_to="crops/%Y/%m/%d/", verbose_name=_("Image"))
    face_id: int = models.IntegerField(null=True, blank=True, verbose_name=_("Face identity"))

    def __str__(self):
        return "{0} ({1})".format(self.face_id, self.uuid)

    class Meta:
        ordering = ("-id", "face_id")
        verbose_name = _("Detected face")
        verbose_name_plural = _("Detected faces")


class SimilarPerson(mixin_models.UUIDModel, mixin_models.TimestampModel):
    """Похожие личности"""

    id: int

    detected_face_id: int
    detected_face: DetectedFace = models.ForeignKey(
        DetectedFace,
        on_delete=models.CASCADE,
        related_name="persons",
        null=False,
        blank=False,
        verbose_name=_("Detected face"),
    )

    photo: str = models.URLField(max_length=1000, verbose_name=_("Photo"))
    distance: float = models.FloatField(null=False, blank=False, verbose_name=_("Distance"))
    first_name: str = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("First name"))
    middle_name: str = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Middle name"))
    last_name: str = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Last name"))
    iin: str = models.CharField(max_length=12, verbose_name=_("Individual identification number"))
    id_number: str = models.CharField(max_length=50, verbose_name=_("ID number"))

    @property
    def fullname(self) -> str:
        return " ".join([self.last_name, self.first_name, self.middle_name])

    def __str__(self):
        return "{0} ({1})".format(self.fullname, self.iin)

    class Meta:
        ordering = ("-distance",)
        verbose_name = _("Similar person")
        verbose_name_plural = _("Similar persons")
