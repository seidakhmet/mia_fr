import base64
import logging
from datetime import datetime

import requests
from django.conf import settings
from django.core.files.base import ContentFile

from django.utils.translation import gettext_lazy as _

from . import models


def detector(original_image_id: int) -> (models.OriginalImage | None, bool):
    original_image = models.OriginalImage.objects.filter(pk=original_image_id).first()
    if not original_image:
        return None, False
    if original_image.results_path and original_image.unique_id and original_image.face_ids:
        return original_image, True
    url = settings.DS_URLS["detector"]
    if original_image.image:
        send_file = {"file": original_image.image.file}
        try:
            response = requests.post(url, files=send_file)
            if response.status_code == 200:
                data = response.json()
                results_date = datetime.utcnow().strftime("%Y%m%d")
                original_image.results_path = results_date
                original_image.unique_id = data.get("unique_id", None)
                original_image.face_ids = data.get("faces", [0])
                original_image.save()
                return original_image, True
            else:
                logging.error(f"Detector error: response status code is {response.status_code}")
                return original_image, False
        except Exception as err:
            logging.error(f"Detector error: {err}")
            return original_image, False
    logging.error(f"Detector error: No file in original image {original_image.uuid}")
    return original_image, False


def get_detected_faces(original_image_id: int) -> (list[models.DetectedFace], bool):
    original_image = models.OriginalImage.objects.filter(pk=original_image_id).first()
    if not original_image:
        return [], False
    detected_faces = []
    if len(original_image.face_ids) == original_image.faces.count():
        for face in original_image.faces.all():
            detected_faces.append(face)
        return detected_faces, True
    try:
        url = settings.DS_URLS["get_detected_faces"]
        response = requests.get(
            url=url, data={"date": original_image.results_path, "unique_id": original_image.unique_id}
        )
        if response.status_code == 200:
            data = response.json()
            for key, value in data.items():
                cfile = ContentFile(base64.b64decode(value), name=f"{original_image.unique_id}_{key}.jpg")
                face, _ = models.DetectedFace.objects.get_or_create(
                    original_image=original_image, face_id=key, image=cfile
                )
                detected_faces.append(face)
            return detected_faces, True
        else:
            logging.error(f"Error in get_detected_faces: response status code is {response.status_code}")
            return [], False
    except Exception as err:
        logging.error(f"Error in get_detected_faces: {err}")
        return original_image, False


def get_metadata(detected_face_id: int) -> (list[models.SimilarPerson], bool):
    detected_face = models.DetectedFace.objects.filter(pk=detected_face_id).first()
    if not detected_face:
        return False
    similar_persons = []
    try:
        url = settings.DS_URLS["get_photo_metadata"]
        params = {
            "date": detected_face.original_image.results_path,
            "unique_id": detected_face.original_image.unique_id,
            "face_id": detected_face.face_id,
            "top": settings.SIMILAR_PERSON_COUNT,
        }
        response = requests.post(url, data=params)
        if response.status_code == 200:
            data = response.json()
            for key, value in data.items():
                person, _ = models.SimilarPerson.objects.get_or_create(
                    detected_face=detected_face,
                    distance=value.get("distance", None),
                    first_name=value.get("firstname", None),
                    last_name=value.get("surname", None),
                    middle_name=value.get("secondname", None),
                    iin=value.get("iin", None),
                    id_number=value.get("ud_number", None),
                )
                similar_persons.append(person)
            return True
        else:
            logging.error(f"Error in get_metadata: response status code is {response.status_code}")
            return False
    except Exception as err:
        logging.error(f"Error in get_metadata: {err}")
        return False
