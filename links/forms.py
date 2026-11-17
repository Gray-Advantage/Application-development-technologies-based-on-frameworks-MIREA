"""Формы поиска и управления короткими ссылками."""

from datetime import date
from urllib.parse import urlsplit

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from .models import Link


class AvailabilityForm(forms.Form):
    date = forms.DateField(
        label="Дата",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    q = forms.CharField(label="Код или URL", required=False, max_length=2048)


class LinkForm(forms.ModelForm):
    url = forms.URLField(
        label="Исходный URL", assume_scheme="https", max_length=2048
    )

    class Meta:
        model = Link
        fields = ("code", "url", "owner", "expires_at", "preview")
        widgets = {
            "expires_at": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
        help_texts = {
            "code": "Латинские буквы, цифры, дефис и подчёркивание.",
            "preview": "PNG, JPEG или WebP размером до 5 МБ.",
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance._state.adding:
            self.instance.created_at = date.today()
        else:
            del self.fields["code"]
            del self.fields["owner"]

    def clean_code(self) -> str:
        code = self.cleaned_data["code"]
        if code in {"available", "statistics"}:
            raise ValidationError(
                "Этот код зарезервирован для страницы сервиса."
            )
        return code

    def clean_url(self) -> str:
        url = self.cleaned_data["url"]
        if urlsplit(url).scheme not in {"http", "https"}:
            raise ValidationError("Используйте адрес HTTP или HTTPS.")
        return url

    def clean_preview(self) -> UploadedFile | bool | None:
        preview = self.cleaned_data["preview"]
        if isinstance(preview, UploadedFile):
            if preview.size > 5 * 1024 * 1024:
                raise ValidationError("Размер изображения превышает 5 МБ.")
            if preview.content_type not in {
                "image/png",
                "image/jpeg",
                "image/webp",
            }:
                raise ValidationError("Поддерживаются PNG, JPEG и WebP.")
        return preview

    def clean(self) -> dict:
        cleaned = super().clean()
        expires_at = cleaned.get("expires_at")
        if expires_at and expires_at <= max(
            self.instance.created_at, date.today()
        ):
            raise ValidationError(
                "Дата окончания должна быть позже даты создания и сегодня."
            )
        return cleaned
