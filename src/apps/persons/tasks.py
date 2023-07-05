from abc import ABC

from celery import Task

from config.celery_app import app

from apps.common.utils.decorators import task_lock
from django.db import transaction

from . import services


class AbstractParserTask(Task, ABC):
    func = None

    def run(self, *args, **kwargs):
        if self.func:
            self.func(*args, **kwargs)


@task_lock()
class FaceRecognitionTask(AbstractParserTask):
    """Таск для запуска распознавания лиц"""

    @transaction.atomic
    def func(self, original_image_id: int):
        original_image, ok = services.detector(original_image_id)
        if ok:
            detected_faces, ok = services.get_detected_faces(original_image_id)
            if ok:
                for face in detected_faces:
                    services.get_metadata(face.id)


face_recognition = app.register_task(FaceRecognitionTask())
