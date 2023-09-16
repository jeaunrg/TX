from django.contrib import admin

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
from .models import Salaire

admin.site.register(Salaire)
admin.site.register(AssApec)
admin.site.register(ComplDecesTA)
admin.site.register(ComplDecesTB)
admin.site.register(ComplTranche1)
admin.site.register(ComplTranche2)
admin.site.register(CsgDeductible)
admin.site.register(SecuSocial)
admin.site.register(SecuSocialPlaf)
