from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.db import transaction
from django.utils.html import escape, format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_object_actions import DjangoObjectActions

from . import models
from . import forms

from . import services
from . import tasks


class ImageInlineAbstract:
    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{1}"><img src="{0}" style="max-height:250px; height: auto;" class="rounded" /></a>'.format(
                    obj.image.url,
                    reverse(
                        "admin:{0}_{1}_change".format(self.model._meta.app_label, self.model._meta.model_name),
                        args=(obj.id,),
                    ),
                )
            )
        else:
            return _("(No photo)")

    image_preview.short_description = _("Photo")


class ReadOnlyAdmin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def image_preview(self, obj: models.OriginalImage):
        if obj.image:
            return format_html(
                '<img src="{0}" style="max-height:350px; height: auto;" class="rounded" />'.format(obj.image.url)
            )
        else:
            return _("(No photo)")

    image_preview.short_description = _("Photo")


@admin.register(models.SimilarPerson)
class SimilarPersonAdmin(admin.ModelAdmin):
    list_display = (
        "distance",
        "first_name",
        "middle_name",
        "last_name",
        "iin",
        "id_number",
    )
    readonly_fields = (
        "original_image_preview",
        "detected_face_preview",
        "photo_preview",
        "distance",
        "first_name",
        "middle_name",
        "last_name",
        "iin",
        "id_number",
    )
    fields = (
        "original_image_preview",
        "detected_face_preview",
        "photo_preview",
        "distance",
        "first_name",
        "middle_name",
        "last_name",
        "iin",
        "id_number",
    )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(detected_face__original_image__request__created_by=request.user)

    def photo_preview(self, obj: models.SimilarPerson):
        if obj.id_number:
            return format_html(
                """<img 
                        src="/udgrphotos/{0}.ldr" 
                        style="max-height:250px; height: 250px;"
                        class="img-fluid mx-auto rounded"
                    />""".format(
                    obj.id_number
                )
            )
        else:
            return _("(No photo)")

    photo_preview.short_description = _("Photo")

    def detected_face_preview(self, obj: models.SimilarPerson):
        if obj.detected_face.image:
            return format_html(
                '<a href="{1}"><img src="{0}" style="max-height:250px; height: auto;" class="rounded"/></a>'.format(
                    obj.detected_face.image.url,
                    reverse("admin:persons_detectedface_change", args=(obj.detected_face.id,)),
                )
            )
        else:
            return _("(No image)")

    detected_face_preview.short_description = _("Detected face")

    def original_image_preview(self, obj: models.SimilarPerson):
        if obj.detected_face.original_image.image:
            return format_html(
                '<a href="{1}"><img src="{0}" style="max-height:250px; height: auto;" class="rounded"/></a>'.format(
                    obj.detected_face.original_image.image.url,
                    reverse("admin:persons_originalimage_change", args=(obj.detected_face.original_image.id,)),
                )
            )
        else:
            return _("(No image)")

    original_image_preview.short_description = _("Original image")


class SimilarPersonInline(ImageInlineAbstract, admin.StackedInline):
    model = models.SimilarPerson
    can_delete = False
    fields = (
        "photo_preview",
        "distance",
        "first_name",
        "middle_name",
        "last_name",
        "iin",
        "id_number",
    )
    readonly_fields = (
        "photo_preview",
        "distance",
        "first_name",
        "middle_name",
        "last_name",
        "iin",
        "id_number",
    )
    template = "admin/similar_persons.html"

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(detected_face__original_image__request__created_by=request.user)

    def photo_preview(self, obj: models.SimilarPerson):
        if obj.id_number:
            return format_html(
                """<img 
                        src="/udgrphotos/{0}.ldr" 
                        style="max-height:250px; height: 250px;"
                        class="img-fluid mx-auto rounded"
                    />""".format(
                    obj.id_number
                )
            )
        else:
            return _("(No photo)")

    photo_preview.short_description = _("Photo")


@admin.register(models.DetectedFace)
class DetectedFaceAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "original_image_preview",
        "max_distance_person",
        "created_at",
    )
    readonly_fields = (
        "uuid",
        "image_preview",
        "face_id",
        "created_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "created_at",
                    "face_id",
                    "original_image_preview",
                    "image_preview",
                )
            },
        ),
    )
    search_fields = (
        "uuid",
        "persons__iin",
    )
    inlines = (SimilarPersonInline,)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(original_image__request__created_by=request.user)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def image_preview(self, obj: models.DetectedFace):
        if obj.image:
            return format_html(
                '<img src="{0}" style="max-height:250px; height: auto;" class="rounded"/>'.format(obj.image.url)
            )
        else:
            return _("(No photo)")

    image_preview.short_description = _("Face")

    def original_image_preview(self, obj: models.DetectedFace):
        if obj.original_image.image:
            return format_html(
                '<a href="{1}"><img src="{0}" style="max-height:250px; height: auto;" class="rounded" /></a>'.format(
                    obj.original_image.image.url,
                    reverse("admin:persons_originalimage_change", args=(obj.original_image.id,)),
                )
            )
        else:
            return _("(No image)")

    original_image_preview.short_description = _("Original image")

    def max_distance_person(self, obj: models.DetectedFace):
        if obj.persons:
            similar_person = obj.persons.first()
            return format_html(
                """<a href="{url}"><div style="position: relative; width:fit-content;">
            <img src="/udgrphotos/{id_number}.ldr" style="max-height:250px; height: 250px;" class="img-fluid mx-auto" />
            <div style="position: absolute;left: 0;bottom: 0;color:white; background:rgba(0, 0, 0, 0.5); opacity:1; width:100%;">
                <small style="display:block;">{iin_trans}: {iin}</small>
                <small style="display:block;">{first_name_trans}: {first_name}</small>
                <small style="display:block;">{last_name_trans}: {last_name}</small>
                <small style="display:block;">{distance_trans}: {distance}%</small>
            </div>
            </div></a>""".format(
                    url=reverse("admin:persons_similarperson_change", args=(similar_person.id,)),
                    id_number=similar_person.id_number,
                    iin=similar_person.iin,
                    first_name=similar_person.first_name,
                    last_name=similar_person.last_name,
                    distance=similar_person.distance,
                    iin_trans=_("IIN"),
                    first_name_trans=_("First name"),
                    last_name_trans=_("Last name"),
                    distance_trans=_("Distance"),
                )
            )
        else:
            return None

    max_distance_person.short_description = _("The similarest person")


class DetectedFaceInline(ImageInlineAbstract, admin.TabularInline):
    model = models.DetectedFace
    can_delete = False
    fields = ("image_preview",)
    readonly_fields = ("image_preview",)
    template = "admin/stacked.html"

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(original_image__request__created_by=request.user)


@admin.register(models.OriginalImage)
class OriginalImageAdmin(DjangoObjectActions, ReadOnlyAdmin, admin.ModelAdmin):
    list_display = (
        "uuid",
        "image_preview",
        "created_at",
    )
    readonly_fields = (
        "uuid",
        "image_preview",
        "unique_id",
        "results_path",
        "face_ids",
        "created_at",
    )
    fields = (
        "request",
        "uuid",
        "created_at",
        "unique_id",
        "results_path",
        "face_ids",
        "image_preview",
    )
    search_fields = (
        "uuid",
        "faces__persons__iin",
    )

    list_filter = (
        "created_at",
        "request__created_by",
    )

    inlines = (DetectedFaceInline,)
    change_form_template = "admin/doa_change_form.html"

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(request__created_by=request.user)

    def face_recognition(self, request, obj: models.OriginalImage):
        tasks.face_recognition.delay(obj.id)
        self.message_user(request, _("Face detection and recognition was started for original image: ") + f"{obj.uuid}")

    face_recognition.label = _("Run face recognition")
    face_recognition.short_description = _("Run face recognition for the original image")

    change_actions = ("face_recognition",)


class OriginalImageInline(ImageInlineAbstract, admin.TabularInline):
    model = models.OriginalImage
    can_delete = False
    fields = ("image_preview",)
    readonly_fields = ("image_preview",)
    extra = 0
    template = "admin/stacked.html"

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(request__created_by=request.user)


@admin.register(models.FaceRecognitionRequest)
class FaceRecognitionRequestAdmin(admin.ModelAdmin):
    readonly_fields = (
        "uuid",
        "created_by",
        "created_at",
    )
    list_display = (
        "uuid",
        "created_by",
        "created_at",
    )
    search_fields = (
        "uuid",
        "images__faces__persons__iin",
    )

    list_filter = (
        "created_at",
        "created_by",
    )

    def get_fieldsets(self, request, obj=None):
        if obj:
            return [
                (
                    None,
                    {
                        "fields": ["uuid", "created_by", "created_at", "description"],
                    },
                ),
            ]
        return [
            (
                None,
                {
                    "fields": ["uuid", "created_by", "created_at", "description", "images"],
                },
            ),
        ]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(created_by=request.user)

    # Inlines
    def get_inlines(self, request, obj=None):
        if obj and obj.images.all().count() > 0:
            return [OriginalImageInline]
        else:
            return []

    # Add form
    add_form = forms.FaceRecognitionRequestAddForm

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    # Save instance
    def save_model(self, request, obj: models.FaceRecognitionRequest, form, change):
        obj.created_by = request.user
        obj.save()

    @transaction.atomic
    def save_form(self, request, form, change):
        if form.is_valid() and not change:
            images = request.FILES.getlist("images")
            response = form.save(commit=True)
            for image in images:
                original_image = models.OriginalImage.objects.create(image=image, request_id=response.pk)
                tasks.face_recognition.delay(original_image_id=original_image.id)

        return form.save(commit=False)

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = "action_time"

    list_filter = ["user", "content_type", "action_flag"]

    search_fields = ["object_repr", "change_message"]

    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_link",
        "action_flag",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse("admin:%s_%s_change" % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return format_html(link)

    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
