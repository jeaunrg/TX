import uuid

from account.models import Account
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

from .calculations import Net


class Salaire(Net):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    impot_is_paid = models.BooleanField("Impôt payé", default=False)
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published"
    )
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

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

    def __repr__(self):
        return (
            f"Salary(brute={self.brute}, "
            f"cotisations={self.all_cotisations}, "
            f"net_imposable={self.net_imposable}, "
            f"net_before_tax={self.net_avant_impot}, "
            f"net={self.net}, "
            f"impot_a_payer={self.impots_a_payer}"
        )

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
            "complementaire",
            "complementaire",
            "complementaire",
            "complementaire",
            "complementaire",
            "complementaire",
            "complementaire",
            "complementaire",
            "complementaire",
        ]
        return [_get_field(field_name) for field_name in display_field_names]


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.author.username}-{instance.uid}")


pre_save.connect(pre_save_blog_post_receiver, sender=Salaire)
