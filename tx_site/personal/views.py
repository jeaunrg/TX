from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .models import Salaire


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "personal/home.html"


class SalaireListView(LoginRequiredMixin, ListView):
    model = Salaire
    paginate_by = 20
    template_name = "personal/list_salaire.html"
    ordering = ["-year", "-month"]
