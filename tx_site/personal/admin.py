from django.contrib import admin

from .models import Contribution, Salaire

admin.site.register(Salaire)
admin.site.register(Contribution)
