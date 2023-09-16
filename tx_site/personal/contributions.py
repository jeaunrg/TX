from django.db import models


# complementaire
class ComplDecesTA(models.Model):
    rate = models.FloatField(default=0.0044)

    def compute(self, netimposable):
        return round(netimposable.base_secu_sociale * self.rate, 2)

    def __str__(self):
        return f"Compl Deces TA {self.rate}"


class ComplDecesTB(models.Model):
    rate = models.FloatField(default=0.0072)

    def compute(self, netimposable):
        return round(netimposable.base_compl_tb * self.rate, 2)


# retraite
class SecuSocialPlaf(models.Model):
    rate = models.FloatField(default=0.069)

    def compute(self, netimposable):
        return round(netimposable.base_secu_sociale * self.rate, 2)


class SecuSocial(models.Model):
    rate = models.FloatField(default=0.004)

    def compute(self, netimposable):
        return round(netimposable.brute * self.rate, 2)


class ComplTranche1(models.Model):
    rate = models.FloatField(default=0.0415)

    def compute(self, netimposable):
        return round(netimposable.base_secu_sociale * 0.0415, 2)


class ComplTranche2(models.Model):
    rate = models.FloatField(default=0.0986)

    def compute(self, netimposable):
        return round(netimposable.base_compl_tb * self.rate, 2)


# chomage
class AssApec(models.Model):
    rate = models.FloatField(default=0.4 * 3 / 5000)

    def compute(self, netimposable):
        return round(netimposable.brute * self.rate, 2)


# contribution sociale generalisee
class CsgDeductible(models.Model):
    rate = models.FloatField(default=0.068)

    def compute(self, netimposable):
        return round(netimposable.base_compl * self.rate, 2)


class CsgCrds(models.Model):
    rate = models.FloatField(default=0.029)

    def compute(self, netimposable):
        return round(netimposable.base_compl * self.rate, 2)
