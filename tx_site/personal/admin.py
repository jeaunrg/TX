from django.contrib import admin

from .models import Contribution, Salaire


class ContributionInline(admin.TabularInline):
    model = Contribution


@admin.register(Salaire)
class SalaireAdmin(admin.ModelAdmin):
    inlines = [ContributionInline]
    exclude = ["date_updated", "date_published", "slug"]

    def get_elements(self, obj):
        return [contribution.name for contribution in obj.contributions.all()]


admin.site.register(Contribution)
