from django.urls import path
from personal.views import SalaireListView

app_name = "personal"

urlpatterns = [
    path("list/", SalaireListView.as_view(), name="list"),
]
