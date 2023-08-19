from django import forms

from .models import Salaire


class SalaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        fields = "__all__"
