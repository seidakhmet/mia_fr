from rest_framework import serializers as drf_serializers
from django.db import transaction
from . import models
from . import tasks


class SimilarPersonSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = models.SimilarPerson
        fields = (
            "uuid",
            "created_at",
            "photo",
            "distance",
            "first_name",
            "middle_name",
            "last_name",
            "iin",
            "id_number",
        )


class DetectedFaceSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = models.DetectedFace
        fields = (
            "uuid",
            "created_at",
            "image",
            "face_id",
        )


class OriginalImageSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = models.OriginalImage
        fields = (
            "uuid",
            "created_at",
            "image",
            "face_ids",
        )


class FaceRecognitionRequestSerializer(drf_serializers.ModelSerializer):
    uploaded_images = drf_serializers.ListField(
        child=drf_serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True
    )

    class Meta:
        model = models.FaceRecognitionRequest
        fields = ("uuid", "created_at", "uploaded_images")

    @transaction.atomic
    def create(self, validated_data):
        uploaded_data = validated_data.pop("uploaded_images")
        request = models.FaceRecognitionRequest.objects.create(
            created_by=self.context["request"].user, **validated_data
        )
        for uploaded_item in uploaded_data:
            original_image = models.OriginalImage.objects.create(request=request, image=uploaded_item)
            tasks.face_recognition.delay(original_image_id=original_image.id)
        return request
