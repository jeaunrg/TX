import uuid

from account.models import Account
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

from tx_site.current_user import get_current_user

from .calculations import *

BASE_CHOICES = [
    ("base_compl", "base_compl"),
    ("brute", "brute"),
]


class Contribution(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    base = models.CharField(max_length=100, choices=BASE_CHOICES, default="brute")
    taux = models.FloatField(default=0.0044)
    is_imposable = models.BooleanField(default=True)
    salaire = models.ForeignKey(
        "Salaire",
        on_delete=models.CASCADE,
        related_name="contributions",
        null=True,
        blank=True,
    )

    @property
    def value(self):
        base_value = self.salaire.brute
        return base_value * self.taux


class Salaire(models.Model):
    uid = models.UUIDField(null=False, primary_key=True, default=uuid.uuid4)
    year = models.IntegerField("year", choices=year_choices(), default=current_year())
    month = models.CharField(
        "month",
        default=current_month(),
        choices=[(m, m) for m in MONTHS],
        max_length=20,
    )
    base_brute = models.FloatField(default=2000.0)
    bonus = models.FloatField(default=0.0)
    rappel = models.FloatField(default=0.0)
    n_absences = models.IntegerField(default=0)
    ticket_resto = models.FloatField(default=80.0)
    navigo = models.FloatField(default=42.0)
    extra_bonus = models.FloatField(default=0.0)
    complementaire = models.FloatField(default=56)
    my_net_avant_impot = models.FloatField(null=True, blank=True)
    taux_prelevement = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2,
    )
    taux_prelevement_theorique = models.DecimalField(
        default=10,
        max_digits=5,
        decimal_places=2,
    )
    my_net = models.FloatField(null=True, blank=True)
    my_impots_a_payer = models.FloatField(null=True, blank=True)
    impot_is_paid = models.BooleanField("Impôt payé", default=False)
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    date_published = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date published",
    )
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    # def __init__(self, *args, **kwargs):
    #     self.uid = uuid.uuid4()
    #     return super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(uuid.uuid4())
        super(Salaire, self).save(*args, **kwargs)

    @property
    def ndays(self):
        month_num = MONTHS.index(self.month) + 1
        return calendar.monthrange(self.year, month_num)[1]

    @property
    def brute_for_absence(self):
        brute_day = self.base_brute / self.ndays
        deducted_absences = self.n_absences * brute_day
        refunded_absences = round(deducted_absences / 2, 2)
        return deducted_absences - refunded_absences

    @property
    def brute(self):
        return self.base_brute + self.bonus + self.rappel - self.brute_for_absence

    @property
    def base_secu_sociale(self):
        work_days_rate = (self.ndays - self.n_absences) / self.ndays
        base_secu_sociale = self.plafond_secu_sociale * work_days_rate
        return base_secu_sociale

    @property
    def cotisations_imposables(self):
        cotisations = [
            contribution.value
            for contribution in self.contributions.all()
            if contribution.is_imposable
        ]
        return sum(cotisations)

    @property
    def net_imposable(self):
        return round(self.brute - self.cotisations_imposables, 2)

    @property
    def cotisations(self):
        cotisations = [
            contribution.value
            for contribution in self.contributions.all()
            if not contribution.is_imposable
        ]
        cotisations += [self.complementaire / 2, self.ticket_resto]
        return sum(cotisations)

    @property
    def all_cotisations(self):
        return sum([contribution.value for contribution in self.contributions.all()])

    @property
    def net_avant_impot(self):
        gain = self.navigo + self.extra_bonus
        return round(self.net_imposable + gain - self.cotisations, 2)

    @property
    def impot(self):
        return self.net_imposable * float(self.taux_prelevement)

    @property
    def impot_theorique(self):
        return self.net_imposable * float(self.taux_prelevement_theorique)

    @property
    def impots_a_payer(self):
        return self.impot_theorique - self.impot

    @property
    def net(self):
        return round(self.net_avant_impot - self.impot, 2)

    @staticmethod
    def header():
        return {
            "year": "Année",
            "month": "Mois",
            "brute": "Salaire brute",
            "net_imposable": "Salaire net imposable",
            "net_avant_impot": "Salaire net avant impot",
            "net": "Salaire net",
            "impots_a_payer": "Impôt restant à payer",
            "edit": "Modifier",
        }

    @property
    def displayed_elements(self):
        def _get_field(field_name):
            value = getattr(self, field_name)
            try:
                name = self._meta.get_field(field_name).verbose_name
            except:
                name = field_name
            return name, value

        display_field_names = [
            "base_brute",
            "compl_deces_ta",
            "compl_deces_tb",
            "complementaire",
            "retraite_secu_sociale_plaf",
            "retraite_secu_sociale",
        ]
        return [_get_field(field_name) for field_name in display_field_names]

    def __repr__(self):
        return (
            f"Salary(brute={self.brute}, "
            f"cotisations={self.all_cotisations}, "
            f"net_imposable={self.net_imposable}, "
            f"net_before_tax={self.net_avant_impot}, "
            f"net={self.net}, "
            f"impot_a_payer={self.impots_a_payer}"
        )


# def pre_save_salaire_receiver(sender, instance, *args, **kwargs):
#     print("slug", instance.slug, instance, type)
#     if not instance.slug:
#         breakpoint()
#         print(instance.uid, instance.author.username)
#         instance.slug = slugify(f"{instance.author.username}-{instance.uid}")


# pre_save.connect(pre_save_salaire_receiver, sender=Salaire)
