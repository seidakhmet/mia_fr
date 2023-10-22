import uuid

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import OuterRef, Subquery
from django.contrib.auth import login, logout, views as auth_views, forms as auth_forms, password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from PIL import Image

from apps.persons.models import DetectedFace, OriginalImage, FaceRecognitionRequest, SimilarPerson

from apps.persons import tasks
from .utils import get_person_by_iin


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control", "id": "floatingInput"})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control", "id": "floatingPassword"}
        ),
    )


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            page = request.GET.get("next", "index")
            return redirect(page)
    else:
        form = CustomAuthenticationForm()
    return render(request, "web/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


@login_required(login_url="login")
@transaction.atomic
def face_recognition_view(request):
    fr_request = FaceRecognitionRequest.objects.create(created_by=request.user)
    original_images = []
    try:
        images = request.FILES.getlist("images")
        for image in images:
            img = Image.open(image)
            original_images.append(OriginalImage.objects.create(image=image, request_id=fr_request.pk))
            img.close()
    except Exception as e:
        fr_request.delete()
        redirect_url = reverse("face-recognition-requests") + f"?message={str(e)}&message_status=0"
        return redirect(redirect_url)

    for original_image in original_images:
        tasks.face_recognition.delay(original_image_id=original_image.id)
    redirect_url = reverse("face-recognition-requests") + f"?message={_('Face recognition request created.')}"
    return redirect(redirect_url)


@login_required(login_url="login")
def face_recognition_requests_view(request):
    queryset = FaceRecognitionRequest.objects.filter(created_by=request.user).order_by("-id")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    message = request.GET.get("message", None)
    message_status = request.GET.get("message_status", 1)

    if start_date:
        queryset = queryset.filter(created_at__gte=start_date)

    if end_date:
        queryset = queryset.filter(created_at__lte=f"{end_date}T23:59:59")

    paginator = Paginator(queryset, 10)
    page = request.GET.get("page", 1)
    items = paginator.get_page(page)
    return render(
        request,
        "web/face_recognition_requests.html",
        context={
            "current_url": "face-recognition-requests",
            "items_count": len(queryset),
            "items": items,
            "current_page": int(page),
            "start_date": start_date,
            "end_date": end_date,
            "message": message,
            "message_status": message_status == 1,
        },
    )


@login_required(login_url="login")
def index_view(request):
    person = None
    queryset = DetectedFace.objects.filter(original_image__request__created_by=request.user)

    requested_iin = request.GET.get("iin")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    message = request.GET.get("message", None)

    if start_date:
        queryset = queryset.filter(original_image__request__created_at__gte=start_date)

    if end_date:
        queryset = queryset.filter(original_image__request__created_at__lte=f"{end_date}T23:59:59")

    if requested_iin:
        queryset = queryset.filter(persons__iin=requested_iin)
        photo = SimilarPerson.objects.filter(detected_face=OuterRef("pk"), iin=requested_iin).values("photo")[:1]
        iin = SimilarPerson.objects.filter(detected_face=OuterRef("pk"), iin=requested_iin).values("iin")[:1]
        first_name = SimilarPerson.objects.filter(detected_face=OuterRef("pk"), iin=requested_iin).values("first_name")[
            :1
        ]
        middle_name = SimilarPerson.objects.filter(detected_face=OuterRef("pk"), iin=requested_iin).values(
            "middle_name"
        )[:1]
        last_name = SimilarPerson.objects.filter(detected_face=OuterRef("pk"), iin=requested_iin).values("last_name")[
            :1
        ]
        distance = SimilarPerson.objects.filter(detected_face=OuterRef("pk"), iin=requested_iin).values("distance")[:1]
        id_number = SimilarPerson.objects.filter(detected_face=OuterRef("pk"), iin=requested_iin).values("id_number")[
            :1
        ]
        person = get_person_by_iin(iin=requested_iin)
    else:
        photo = SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("photo")[:1]
        iin = SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("iin")[:1]
        first_name = (
            SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("first_name")[:1]
        )
        middle_name = (
            SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("middle_name")[:1]
        )
        last_name = (
            SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("last_name")[:1]
        )
        distance = (
            SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("distance")[:1]
        )
        id_number = (
            SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("id_number")[:1]
        )
    queryset = queryset.annotate(
        photo=Subquery(photo),
        iin=Subquery(iin),
        first_name=Subquery(first_name),
        middle_name=Subquery(middle_name),
        last_name=Subquery(last_name),
        distance=Subquery(distance),
        id_number=Subquery(id_number),
    )

    paginator = Paginator(queryset, 10)
    page = request.GET.get("page", 1)
    items = paginator.get_page(page)
    return render(
        request,
        "web/index.html",
        context={
            "current_url": "index",
            "items_count": len(queryset),
            "items": items,
            "current_page": int(page),
            "start_date": start_date,
            "end_date": end_date,
            "message": message,
            "iin": requested_iin,
            "person": person,
        },
    )


@login_required(login_url="login")
def original_image_detail_view(request, image_uuid: uuid.UUID):
    queryset = OriginalImage.objects.filter(request__created_by=request.user)
    image = queryset.filter(uuid=image_uuid).first()
    if image is None:
        return render(
            request,
            "web/404.html",
        )

    photo = SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("photo")[:1]
    iin = SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("iin")[:1]
    first_name = (
        SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("first_name")[:1]
    )
    middle_name = (
        SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("middle_name")[:1]
    )
    last_name = SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("last_name")[:1]
    distance = SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("distance")[:1]
    id_number = SimilarPerson.objects.filter(detected_face=OuterRef("pk")).order_by("-distance").values("id_number")[:1]

    items = DetectedFace.objects.filter(original_image=image).annotate(
        photo=Subquery(photo),
        iin=Subquery(iin),
        first_name=Subquery(first_name),
        middle_name=Subquery(middle_name),
        last_name=Subquery(last_name),
        distance=Subquery(distance),
        id_number=Subquery(id_number),
    )
    return render(
        request,
        "web/original_image_detail.html",
        context={"original_image": image, "fr_request": image.request, "items": items},
    )


@login_required(login_url="login")
def face_detail_view(request, face_uuid: uuid.UUID):
    queryset = DetectedFace.objects.filter(original_image__request__created_by=request.user)
    face = queryset.filter(uuid=face_uuid).first()
    if face is None:
        return render(
            request,
            "web/404.html",
        )
    return render(
        request,
        "web/face_detail.html",
        context={
            "face": face,
            "persons": face.persons.all(),
            "original_image": face.original_image,
            "fr_request": face.original_image.request,
            "image_faces": face.original_image.faces.all().order_by("face_id"),
        },
    )


class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control", "id": "floatingNewPassword1"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control", "id": "floatingNewPassword2"}
        ),
    )
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
                "id": "floatingOldPassword",
            }
        ),
    )


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "web/change_password.html"
    success_url = reverse_lazy("logout")
