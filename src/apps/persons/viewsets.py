import uuid as _uuid
from rest_framework import (
    viewsets as drf_viewsets,
    mixins as drf_mixins,
    response as drf_response,
    status as drf_status,
)
from rest_framework.decorators import action

from . import models
from . import serializers
from . import tasks


class FaceRecognitionRequestViewSet(
    drf_viewsets.GenericViewSet, drf_mixins.CreateModelMixin, drf_mixins.ListModelMixin, drf_mixins.RetrieveModelMixin
):
    queryset = models.FaceRecognitionRequest.objects.all()
    serializer_class = serializers.FaceRecognitionRequestSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return drf_response.Response(serializer.data, status=drf_status.HTTP_201_CREATED, headers=headers)

    @action(methods=["GET"], detail=True, url_path="images")
    def images(self, request, uuid: _uuid.UUID | None = None, *args, **kwargs):
        data = models.OriginalImage.objects.filter(request__uuid=uuid)
        serializer = serializers.OriginalImageSerializer(data, many=True)
        return drf_response.Response(serializer.data, status=drf_status.HTTP_200_OK)


class OriginalImageViewSet(drf_viewsets.GenericViewSet, drf_mixins.ListModelMixin, drf_mixins.RetrieveModelMixin):
    queryset = models.OriginalImage.objects.all()
    serializer_class = serializers.OriginalImageSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(request__created_by=self.request.user)

    @action(methods=["GET"], detail=True, url_path="faces")
    def faces(self, request, uuid: _uuid.UUID | None = None, *args, **kwargs):
        data = models.DetectedFace.objects.filter(original_image__uuid=uuid)
        serializer = serializers.DetectedFaceSerializer(data, many=True)
        return drf_response.Response(serializer.data, status=drf_status.HTTP_200_OK)

    @action(methods=["GET"], detail=True, url_path="recognition")
    def recognition(self, request, uuid: _uuid.UUID | None = None, *args, **kwargs):
        instance = self.get_object()
        if instance.faces:
            return drf_response.Response(
                {"status": False, "detail": "Facial recognition has already been performed."},
                status=drf_status.HTTP_200_OK,
            )
        tasks.face_recognition.delay(instance.id)
        return drf_response.Response(
            {"status": True, "detail": "Facial detection is in progress."}, status=drf_status.HTTP_200_OK
        )


class DetectedFaceViewSet(drf_viewsets.GenericViewSet, drf_mixins.ListModelMixin, drf_mixins.RetrieveModelMixin):
    queryset = models.DetectedFace.objects.all()
    serializer_class = serializers.DetectedFaceSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(original_image__request__created_by=self.request.user)

    @action(methods=["GET"], detail=True, url_path="persons")
    def persons(self, request, uuid: _uuid.UUID | None = None, *args, **kwargs):
        data = models.SimilarPerson.objects.filter(detected_face__uuid=uuid)
        serializer = serializers.SimilarPersonSerializer(data, many=True)
        return drf_response.Response(serializer.data, status=drf_status.HTTP_200_OK)


class SimilarPersonViewSet(drf_viewsets.GenericViewSet, drf_mixins.ListModelMixin, drf_mixins.RetrieveModelMixin):
    queryset = models.SimilarPerson.objects.all()
    serializer_class = serializers.SimilarPersonSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(detected_face__original_image__request__created_by=self.request.user)
