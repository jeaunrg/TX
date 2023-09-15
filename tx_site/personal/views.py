from account.models import Account
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import SalaireForm
from .models import Salaire


class HomePageView(LoginRequiredMixin, ListView):
    model = Salaire
    paginate_by = 20
    template_name = "personal/list_salaire.html"
    ordering = ["-year", "-month"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = self.model.header()
        return context


class SalaireCreateView(LoginRequiredMixin, CreateView):
    form_class = SalaireForm
    template_name = "personal/create_salaire.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Account.objects.filter(
            username=self.request.user.username
        ).first()
        self.object.save()
        return redirect("personal:list")


class SalaireEditView(LoginRequiredMixin, UpdateView):
    model = Salaire
    form_class = SalaireForm
    template_name = "personal/edit_salaire.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.author:
            return redirect("personal:detail", obj.slug)
        return UpdateView.dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return redirect("personal:list")


class SalaireDetailView(LoginRequiredMixin, DetailView):
    model = Salaire
    template_name = "personal/detail_salaire.html"


class SalaireDeleteView(DeleteView):
    model = Salaire
    template_name = "personal/confirm_delete_salaire.html"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
