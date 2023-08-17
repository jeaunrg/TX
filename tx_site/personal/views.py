from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "personal/home.html"
