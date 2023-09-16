from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .contributions import *


@receiver(post_migrate)
def create_default_csg_crds(sender, **kwargs):
    if sender.name == "personal":
        ComplDecesTA.objects.create()
        ComplDecesTB.objects.create()
        SecuSocialPlaf.objects.create()
        SecuSocial.objects.create()
        ComplTranche1.objects.create()
        ComplTranche2.objects.create()
        AssApec.objects.create()
        CsgDeductible.objects.create()
        CsgCrds.objects.create()
