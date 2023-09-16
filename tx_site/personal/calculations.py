import calendar
import datetime

from django.db import models

from .contributions import (
    AssApec,
    ComplDecesTA,
    ComplDecesTB,
    ComplTranche1,
    ComplTranche2,
    CsgDeductible,
    SecuSocial,
    SecuSocialPlaf,
)

MONTHS = calendar.month_name[1:]


def year_choices():
    return [(r, r) for r in range(1970, datetime.date.today().year + 100)]


def current_year():
    return datetime.date.today().year


def get_next_month(month: str, year: int) -> str:
    index = MONTHS.index(month)
    if index + 1 == len(MONTHS):
        return MONTHS[0], year + 1
    else:
        return MONTHS[index + 1], year


def current_month():
    month_num = datetime.date.today().month
    return calendar.month_name[month_num]


class Base(models.Model):
    year = models.IntegerField("year", choices=year_choices(), default=current_year())
    month = models.CharField(
        "month",
        default=current_month(),
        choices=[(m, m) for m in MONTHS],
        max_length=20,
    )

    @property
    def ndays(self):
        month_num = MONTHS.index(self.month) + 1
        return calendar.monthrange(self.year, month_num)[1]


class Brute(Base):
    base_brute = models.FloatField(default=2000.0)
    bonus = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    n_absences = models.IntegerField(default=0)
    my_brute = models.FloatField(null=True, blank=True)

    @property
    def brute_for_absence(self):
        brute_day = self.base_brute / self.ndays
        deducted_absences = self.n_absences * brute_day
        refunded_absences = round(deducted_absences / 2, 2)
        return deducted_absences - refunded_absences

    @property
    def brute(self):
        return self.base_brute + self.bonus + self.recall - self.brute_for_absence


class NetImposable(Brute):
    plafond_secu_sociale = models.FloatField(default=3666)
    compl_deces_ta = models.ForeignKey(
        ComplDecesTA, on_delete=models.CASCADE, related_name="netimposable"
    )
    compl_deces_tb = models.ForeignKey(
        ComplDecesTB, on_delete=models.CASCADE, related_name="netimposable"
    )
    complementaire = models.FloatField(default=56)
    retraite_secu_sociale_plaf = models.ForeignKey(
        SecuSocialPlaf, on_delete=models.CASCADE, related_name="netimposable"
    )
    retraite_secu_sociale = models.ForeignKey(
        SecuSocial, on_delete=models.CASCADE, related_name="netimposable"
    )
    retraite_compl1 = models.ForeignKey(
        ComplTranche1, on_delete=models.CASCADE, related_name="netimposable"
    )
    retraite_compl2 = models.ForeignKey(
        ComplTranche2, on_delete=models.CASCADE, related_name="netimposable"
    )
    ass_chomage_apec = models.ForeignKey(
        AssApec, on_delete=models.CASCADE, related_name="netimposable"
    )
    rate_compl_cotisation_pat = models.FloatField(default=0.495)
    rate_base_compl_part_brute = models.FloatField(default=0.9825)
    csg_deductible = models.ForeignKey(
        CsgDeductible, on_delete=models.CASCADE, related_name="netimposable"
    )
    my_net_imposable = models.FloatField(null=True, blank=True)

    @property
    def base_secu_sociale(self):
        work_days_rate = (self.ndays - self.n_absences) / self.ndays
        return self.plafond_secu_sociale * work_days_rate

    @property
    def compl_cotisation_pat(self):
        compl_deces = self.compl_deces_ta.compute(self) + self.compl_deces_tb.compute(
            self
        )
        return self.complementaire / 2 + compl_deces * (
            1 / self.rate_compl_cotisation_pat - 1
        )

    @property
    def base_compl_tb(self):
        return self.brute - self.base_secu_sociale

    @property
    def base_compl(self):
        return self.brute * self.rate_base_compl_part_brute + self.compl_cotisation_pat

    @property
    def cotisations(self):
        cotisations = [
            self.compl_deces_ta.compute(self),
            self.compl_deces_tb.compute(self),
            self.retraite_secu_sociale_plaf.compute(self),
            self.retraite_secu_sociale.compute(self),
            self.retraite_compl1.compute(self),
            self.retraite_compl2.compute(self),
            self.ass_chomage_apec.compute(self),
            self.csg_deductible.compute(self),
        ]
        return sum(cotisations)

    @property
    def net_imposable(self):
        return round(self.brute - self.cotisations, 2)


class NetAvantImpot(NetImposable):
    ticket_resto = models.FloatField(default=80.0)
    navigo = models.FloatField(default=42.0)
    extra_bonus = models.FloatField(default=0.0)
    my_net_avant_impot = models.FloatField(null=True, blank=True)

    @property
    def csg_crds(self):
        rate = 0.029
        return round(self.base_compl * rate, 2)

    @property
    def all_cotisations(self):
        return self.cotisations + self.complementaire / 2 + self.csg_crds

    @property
    def net_avant_impot(self):
        gain = self.navigo + self.extra_bonus
        retenue = self.csg_crds + self.complementaire / 2 + self.ticket_resto
        return round(self.net_imposable + gain - retenue, 2)


class Net(NetAvantImpot):
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
