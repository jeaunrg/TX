import calendar
from datetime import datetime
from typing import Optional

from utils import round_down


class Brute:
    def __init__(self, month_num, year, base_brute, bonus, n_absences, recall):
        self.base_brute = base_brute
        self.bonus = bonus
        self.n_absences = n_absences

        self.recall = recall
        self.month_num = month_num
        self.year = year
        self.month = datetime.strptime(str(month_num), "%m").strftime("%B")
        self.ndays = calendar.monthrange(year, month_num)[1]

    @property
    def brute_for_absence(self):
        brute_day = self.base_brute / self.ndays
        deducted_absences = self.n_absences * brute_day
        refunded_absences = round_down(deducted_absences / 2, 2)
        return deducted_absences - refunded_absences

    @property
    def brute(self):
        return self.base_brute + self.bonus + self.recall - self.brute_for_absence


class NetImposable(Brute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.complementaire = 56 / 2

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
        return self.complementaire + compl_deces * (1 / rate - 1)

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
    def __init__(
        self,
        ticket_resto: int = 0,
        navigo: int = 0,
        extra_bonus: int = 0,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.ticket_resto = ticket_resto
        self.navigo = navigo
        self.extra_bonus = extra_bonus

    @property
    def csg_crds(self):
        rate = 0.029
        return round(self.base_compl * rate, 2)

    @property
    def all_cotisations(self):
        return self.cotisations + self.complementaire + self.csg_crds

    @property
    def net_avant_impot(self):
        gain = self.navigo + self.extra_bonus
        retenue = self.csg_crds + self.complementaire + self.ticket_resto
        return round(self.net_imposable + gain - retenue, 2)


class Salaire(NetAvantImpot):
    def __init__(
        self,
        taux_prelevement: float = 0,
        taux_prelevement_theorique: float = 0.10,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.taux_prelevement = taux_prelevement
        self.impot = self.net_imposable * self.taux_prelevement
        self.taux_prelevement_theorique = taux_prelevement_theorique
        self.impot_theorique = self.net_imposable * self.taux_prelevement_theorique
        self.impots_a_payer = self.impot_theorique - self.impot
        self.impot_is_paid = False

    @property
    def net(self):
        return round(self.net_avant_impot - self.impot, 2)

    def __repr__(self):
        return (
            f"Salary(brute={self.brute}, "
            f"cotisations={self.all_cotisations}, "
            f"net_imposable={self.net_imposable}, "
            f"net_before_tax={self.net_avant_impot}, "
            f"net={self.net}, "
            f"impot_a_payer={self.impots_a_payer}"
        )


class Salaires:
    def __init__(self):
        self.annual_brute = 0
        self.annual_bonus = 0
        self.bonus_recurrence = 0
        self._no_bonus_count = 0
        self.year = 1970
        self.month_num = 0
        self.ticket_resto = 0
        self.navigo = 0.0
        self.taux_prelevement = 0.0
        self.taux_prelevement_theorique = 0.10
        self.salaries = []

    def add_salary(
        self,
        force_get_bonus: bool = False,
        n_absences: int = 0,
        extra_bonus: int = 0,
        recall: float = 0,
        annual_brute: Optional[int] = None,
        annual_bonus: Optional[int] = None,
        bonus_recurrence: Optional[int] = None,
        year: Optional[int] = None,
        month_num: Optional[int] = None,
        ticket_resto: Optional[int] = None,
        navigo: Optional[float] = None,
        taux_prelevement: Optional[float] = None,
        taux_prelevement_theorique: Optional[float] = None,
    ) -> Salaire:
        if annual_brute is not None:
            self.annual_brute = annual_brute
        if annual_bonus is not None:
            self.annual_bonus = annual_bonus
        if bonus_recurrence is not None:
            self.bonus_recurrence = bonus_recurrence

        self._no_bonus_count += 1
        if force_get_bonus:
            self._no_bonus_count = self.bonus_recurrence

        salary = Salaire(
            year=year or self.year,
            n_absences=n_absences,
            extra_bonus=extra_bonus,
            recall=recall,
            base_brute=self.annual_brute / 12,
            bonus=self.current_bonus,
            month_num=month_num or self.month_num + 1,
            ticket_resto=ticket_resto or self.ticket_resto,
            navigo=navigo or self.navigo,
            taux_prelevement=taux_prelevement or self.taux_prelevement,
            taux_prelevement_theorique=taux_prelevement_theorique
            or self.taux_prelevement_theorique,
        )
        self.update_default(salary)
        self.salaries.append(salary)
        print(salary)
        return salary

    def update_default(self, salary: Salaire):
        self.year = salary.year
        self.month_num = salary.month_num
        self.ticket_resto = salary.ticket_resto
        self.navigo = salary.navigo
        self.taux_prelevement = salary.taux_prelevement
        self.taux_prelevement_theorique = salary.taux_prelevement_theorique

    @property
    def current_bonus(self):
        if self._no_bonus_count >= self.bonus_recurrence:
            self._no_bonus_count = 0
            return self.annual_bonus / (12 / self.bonus_recurrence)
        return 0

    @property
    def impots_a_payer(self):
        return round(
            sum([salary.impots_a_payer for salary in self.salaries if not salary.impot_is_paid]),
            2,
        )


if __name__ == "__main__":
    salaries = Salaires()
    salary = salaries.add_salary(
        year=2023,
        annual_brute=42000,
        annual_bonus=3000,
        bonus_recurrence=3,
        force_get_bonus=True,
        ticket_resto=110,
        navigo=42.05,
        taux_prelevement=0.012,
        taux_prelevement_theorique=0.09,
    )
    salary.impot_is_paid = True
    salary = salaries.add_salary(ticket_resto=95)
    salary = salaries.add_salary(ticket_resto=105, taux_prelevement=0.094)
    salary = salaries.add_salary(ticket_resto=80, annual_brute=42420, n_absences=3, recall=35)
    salary = salaries.add_salary(ticket_resto=70, taux_prelevement=0.105, extra_bonus=1000)

    print(f"Impots à payer: {salaries.impots_a_payer}")
