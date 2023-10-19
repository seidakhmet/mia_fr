from django.urls import path, include
from rest_framework import routers

from apps.persons.viewsets import (
    FaceRecognitionRequestViewSet,
    OriginalImageViewSet,
    DetectedFaceViewSet,
    SimilarPersonViewSet,
)


router = routers.DefaultRouter()


router.register("request", FaceRecognitionRequestViewSet, basename="face-recognition-request")
router.register("image", OriginalImageViewSet, basename="original-image")
router.register("faces", DetectedFaceViewSet, basename="detected-face")
router.register("persons", SimilarPersonViewSet, basename="similar-person")


urlpatterns = [
    path("v1/", include(router.urls)),
]
