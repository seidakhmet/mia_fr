from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from . import models


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if not data or len(data) == 0:
            raise forms.ValidationError(_("No files selected."))
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FaceRecognitionRequestAddForm(forms.ModelForm):
    files = MultipleFileField(
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"])],
        label=_("Images"),
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label=_("Description"),
    )

    class Meta:
        model = models.FaceRecognitionRequest
        fields = [
            "files",
            "description",
        ]
