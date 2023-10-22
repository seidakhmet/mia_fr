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
    path("", views.index_view, name="index"),
    path("face-recognition-requests", views.face_recognition_requests_view, name="face-recognition-requests"),
    path("face-recognition", views.face_recognition_view, name="face-recognition"),
    path("face-detail/<uuid:face_uuid>", views.face_detail_view, name="face-detail"),
    path("image-detail/<uuid:image_uuid>", views.original_image_detail_view, name="image-detail"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.CustomPasswordChangeView.as_view(), name="password-change"),
]
