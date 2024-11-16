from django.forms import ModelForm, CheckboxSelectMultiple, ModelMultipleChoiceField, BooleanField, SelectMultiple

from graph_recsys.models import Genre, Prefer

class StyleFormMixin:
    """
    класс-миксин для стилизации форм
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs={'size': '5'}
            field.widget.attrs['class'] = "form-check-input"
            field.widget.attrs['class'] = "form-control-lg"


class PreferForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Prefer
        fields = ('genres',)
        genres = ModelMultipleChoiceField(
            queryset=Genre.objects.all(),
            widget=SelectMultiple(),

        )
