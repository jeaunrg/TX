from django.urls import path
from personal.views import SalaireListView, SalaireCreateView

app_name = "personal"

urlpatterns = [
    path("list/", SalaireListView.as_view(), name="list"),
    path("create/", SalaireCreateView.as_view(), name="create"),
]
