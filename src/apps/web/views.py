from django.shortcuts import render

from apps.persons.models import DetectedFace, OriginalImage, FaceRecognitionRequest


def index(request):
    faces = DetectedFace.objects.all()
    images = OriginalImage.objects.all()
    fr_requests = FaceRecognitionRequest.objects.all()
    return render(request, 'web/index.html', context={'faces': faces, 'images': images, 'fr_requests': fr_requests})
