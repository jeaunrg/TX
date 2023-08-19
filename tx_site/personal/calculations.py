import calendar
import datetime
import uuid

from account.models import Account
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify


def year_choices():
    return [(r, r) for r in range(1970, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


MONTH_CHOICES = [(m, m) for m in calendar.month_name[1:]]


def current_month():
    month_num = datetime.date.today().month
    return calendar.month_name[month_num]


class Base(models.Model):
    year = models.IntegerField("year", choices=year_choices(), default=current_year())
    month = models.CharField(
        "month",
        default=current_month(),
        choices=MONTH_CHOICES,
        max_length=20,
    )

    @property
    def ndays(self):
        month_num = MONTH_CHOICES.index((self.month, self.month)) + 1
        return calendar.monthrange(self.year, month_num)[1]


class Brute(Base):
    base_brute = models.FloatField(default=2000.0)
    bonus = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    n_absences = models.IntegerField(default=0)

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
    complementaire = models.FloatField(default=56)

    @property
    def _base_secu_sociale(self):
        plafond = 3666
        work_days_rate = (self.ndays - self.n_absences) / self.ndays
        return plafond * work_days_rate

    @property
    def _base_compl_tb(self):
        return self.brute - self._base_secu_sociale

    @property
    def compl_deces_tb(self):
        rate = 0.0072
        return round(self._base_compl_tb * rate, 2)

    @property
    def compl_deces_ta(self):
        rate = 0.0044
        return round(self._base_secu_sociale * rate, 2)

    @property
    def _compl_cotisation_pat(self):
        rate = 0.495
        compl_deces = self.compl_deces_ta + self.compl_deces_tb
        return self.complementaire / 2 + compl_deces * (1 / rate - 1)

    @property
    def base_compl(self):
        rate_part_brute = 0.9825
        return self._compl_cotisation_pat + self.brute * rate_part_brute

    @property
    def cotisations(self):
        retraite_secu_sociale_plaf = round(self._base_secu_sociale * 0.069, 2)
        retraite_secu_sociale = round(self.brute * 0.004, 2)
        csg_deductible = round(self.base_compl * 0.068, 2)
        ass_chomage_apec = round(self.brute * 0.4 * 3 / 5000, 2)
        retraite_compl1 = round(self._base_secu_sociale * 0.0415, 2)
        retraite_compl2 = round(self._base_compl_tb * 0.0986, 2)
        cotisations = [
            self.compl_deces_ta,
            self.compl_deces_tb,
            retraite_secu_sociale_plaf,
            retraite_secu_sociale,
            retraite_compl1,
            retraite_compl2,
            ass_chomage_apec,
            csg_deductible,
        ]
        return sum(cotisations)

    @property
    def net_imposable(self):
        return round(self.brute - self.cotisations, 2)


class NetAvantImpot(NetImposable):
    ticket_resto = models.FloatField(default=80.0)
    navigo = models.FloatField(default=42.0)
    extra_bonus = models.FloatField(default=0.0)

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
