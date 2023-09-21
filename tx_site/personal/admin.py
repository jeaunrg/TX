from django.contrib import admin

from .models import Contribution, Salaire


class ContributionInline(admin.TabularInline):
    model = Contribution
    extra = 10


@admin.register(Salaire)
class SalaireAdmin(admin.ModelAdmin):
    inlines = [ContributionInline]
    exclude = ["date_updated", "date_published", "slug"]


admin.site.register(Contribution)
