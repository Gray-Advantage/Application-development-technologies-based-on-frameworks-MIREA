"""GET-фильтры журнала переходов."""

from django import forms

from links.models import Link
from users.models import User


class ClickFilterForm(forms.Form):
    date = forms.DateField(
        label="Дата",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    q = forms.CharField(label="Поиск", required=False, max_length=200)
    owner = forms.ModelChoiceField(
        label="Владелец",
        queryset=User.objects.order_by("username"),
        empty_label="Все",
        required=False,
    )
    code = forms.ModelChoiceField(
        label="Ссылка",
        queryset=Link.objects.order_by("code"),
        empty_label="Все",
        required=False,
    )
    sort = forms.ChoiceField(
        label="Порядок",
        required=False,
        choices=(
            ("date", "По дате"),
            ("-date", "Сначала новые"),
            ("code", "По ссылке"),
            ("owner", "По владельцу"),
        ),
    )
    active = forms.BooleanField(
        label="Только включённые ссылки", required=False
    )

    def query_params(self) -> dict:
        """Параметры запроса из проверенных полей и выбранных объектов."""
        params = self.cleaned_data.copy()
        if params["owner"]:
            params["owner"] = params["owner"].pk
        if params["code"]:
            params["code"] = params["code"].pk
        params["active"] = "1" if params["active"] else ""
        return params
