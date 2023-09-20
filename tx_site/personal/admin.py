from django.contrib import admin

from .models import Contribution, ContributionImposable, Salaire


class ContributionImposableInline(admin.TabularInline):
    model = ContributionImposable


class ContributionInline(admin.TabularInline):
    model = Contribution


@admin.register(Salaire)
class SalaireAdmin(admin.ModelAdmin):
    inlines = [ContributionImposableInline, ContributionInline]
    exclude = ["date_updated", "date_published", "slug"]

    def get_elements(self, obj):
        return [element.name for element in obj.elements_imposable.all()]


admin.site.register(Contribution)
