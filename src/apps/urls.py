from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.persons.viewsets import (
    FaceRecognitionRequestViewSet,
    OriginalImageViewSet,
    DetectedFaceViewSet,
    SimilarPersonViewSet,
)
from apps.web import views

router = routers.DefaultRouter()

router.register("request", FaceRecognitionRequestViewSet, basename="face-recognition-request")
router.register("image", OriginalImageViewSet, basename="original-image")
router.register("faces", DetectedFaceViewSet, basename="detected-face")
router.register("persons", SimilarPersonViewSet, basename="similar-person")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", views.index, name="index"),
]
