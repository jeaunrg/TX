from django import forms

from .models import Salaire


class SalaireForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_model_choice_empty_label()

    def remove_model_choice_empty_label(self):
        for field in self.fields.values():
            if isinstance(field, forms.ModelChoiceField):
                field.empty_label = None

    class Meta:
        model = Salaire
        fields = "__all__"
        exclude = ["slug", "author", "date_updated", "date_published"]
