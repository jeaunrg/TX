from django.urls import path
from personal.views import (
    HomePageView,
    SalaireCreateView,
    SalaireDeleteView,
    SalaireDetailView,
    SalaireEditView,
)

app_name = "personal"

urlpatterns = [
    path("list/", HomePageView.as_view(), name="list"),
    path("create/", SalaireCreateView.as_view(), name="create"),
    path("<slug>/", SalaireDetailView.as_view(), name="detail"),
    path("<slug>/edit/", SalaireEditView.as_view(), name="edit"),
    path("<slug>/delete/", SalaireDeleteView.as_view(), name="delete"),
]
