from account.models import Account
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import ContributionForm, SalaireForm
from .models import Contribution, Salaire


class HomePageView(LoginRequiredMixin, ListView):
    model = Salaire
    paginate_by = 20
    template_name = "personal/list_salaire.html"
    ordering = ["year", "month"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = self.model.header()
        return context


class SalaireCreateView(LoginRequiredMixin, CreateView):
    form_class = SalaireForm
    template_name = "personal/create_salaire.html"

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.request.user.parameters)
        contribution = Contribution()
        contribution.save()
        initial["contributions"] = [contribution]
        return initial

    def form_valid(self, form):
        self.salaire: Salaire = form.save(commit=False)
        self.salaire.author = Account.objects.filter(
            username=self.request.user.username
        ).first()
        self.salaire.save()
        self.salaire.author.update_default_salaire(form)
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
        self.object.author.update_default_salaire(form)
        return redirect("personal:list")


class SalaireDetailView(LoginRequiredMixin, DetailView):
    model = Salaire
    template_name = "personal/detail_salaire.html"


class SalaireDeleteView(LoginRequiredMixin, DeleteView):
    model = Salaire
    template_name = "personal/confirm_delete_salaire.html"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ContributionCreateView(LoginRequiredMixin, CreateView):
    model = Contribution
    form_class = ContributionForm
    template_name = "personal/create_contribution.html"
    success_url = "/"

    def form_valid(self, form):
        slug = self.kwargs["slug"]
        form.instance.salaire = Salaire.objects.get(slug=slug)
        return super().form_valid(form)
