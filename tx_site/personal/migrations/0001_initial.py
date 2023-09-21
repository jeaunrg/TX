# Generated by Django 4.2.4 on 2023-09-21 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tx_site.current_user
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contribution",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "base",
                    models.CharField(
                        choices=[("base_compl", "base_compl"), ("brute", "brute")],
                        default="brute",
                        max_length=100,
                    ),
                ),
                ("taux", models.FloatField(default=0.0044)),
                ("is_imposable", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Salaire",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "year",
                    models.IntegerField(
                        choices=[
                            (1970, 1970),
                            (1971, 1971),
                            (1972, 1972),
                            (1973, 1973),
                            (1974, 1974),
                            (1975, 1975),
                            (1976, 1976),
                            (1977, 1977),
                            (1978, 1978),
                            (1979, 1979),
                            (1980, 1980),
                            (1981, 1981),
                            (1982, 1982),
                            (1983, 1983),
                            (1984, 1984),
                            (1985, 1985),
                            (1986, 1986),
                            (1987, 1987),
                            (1988, 1988),
                            (1989, 1989),
                            (1990, 1990),
                            (1991, 1991),
                            (1992, 1992),
                            (1993, 1993),
                            (1994, 1994),
                            (1995, 1995),
                            (1996, 1996),
                            (1997, 1997),
                            (1998, 1998),
                            (1999, 1999),
                            (2000, 2000),
                            (2001, 2001),
                            (2002, 2002),
                            (2003, 2003),
                            (2004, 2004),
                            (2005, 2005),
                            (2006, 2006),
                            (2007, 2007),
                            (2008, 2008),
                            (2009, 2009),
                            (2010, 2010),
                            (2011, 2011),
                            (2012, 2012),
                            (2013, 2013),
                            (2014, 2014),
                            (2015, 2015),
                            (2016, 2016),
                            (2017, 2017),
                            (2018, 2018),
                            (2019, 2019),
                            (2020, 2020),
                            (2021, 2021),
                            (2022, 2022),
                            (2023, 2023),
                            (2024, 2024),
                            (2025, 2025),
                            (2026, 2026),
                            (2027, 2027),
                            (2028, 2028),
                            (2029, 2029),
                            (2030, 2030),
                            (2031, 2031),
                            (2032, 2032),
                            (2033, 2033),
                            (2034, 2034),
                            (2035, 2035),
                            (2036, 2036),
                            (2037, 2037),
                            (2038, 2038),
                            (2039, 2039),
                            (2040, 2040),
                            (2041, 2041),
                            (2042, 2042),
                            (2043, 2043),
                            (2044, 2044),
                            (2045, 2045),
                            (2046, 2046),
                            (2047, 2047),
                            (2048, 2048),
                            (2049, 2049),
                            (2050, 2050),
                            (2051, 2051),
                            (2052, 2052),
                            (2053, 2053),
                            (2054, 2054),
                            (2055, 2055),
                            (2056, 2056),
                            (2057, 2057),
                            (2058, 2058),
                            (2059, 2059),
                            (2060, 2060),
                            (2061, 2061),
                            (2062, 2062),
                            (2063, 2063),
                            (2064, 2064),
                            (2065, 2065),
                            (2066, 2066),
                            (2067, 2067),
                            (2068, 2068),
                            (2069, 2069),
                            (2070, 2070),
                            (2071, 2071),
                            (2072, 2072),
                            (2073, 2073),
                            (2074, 2074),
                            (2075, 2075),
                            (2076, 2076),
                            (2077, 2077),
                            (2078, 2078),
                            (2079, 2079),
                            (2080, 2080),
                            (2081, 2081),
                            (2082, 2082),
                            (2083, 2083),
                            (2084, 2084),
                            (2085, 2085),
                            (2086, 2086),
                            (2087, 2087),
                            (2088, 2088),
                            (2089, 2089),
                            (2090, 2090),
                            (2091, 2091),
                            (2092, 2092),
                            (2093, 2093),
                            (2094, 2094),
                            (2095, 2095),
                            (2096, 2096),
                            (2097, 2097),
                            (2098, 2098),
                            (2099, 2099),
                            (2100, 2100),
                            (2101, 2101),
                            (2102, 2102),
                            (2103, 2103),
                            (2104, 2104),
                            (2105, 2105),
                            (2106, 2106),
                            (2107, 2107),
                            (2108, 2108),
                            (2109, 2109),
                            (2110, 2110),
                            (2111, 2111),
                            (2112, 2112),
                            (2113, 2113),
                            (2114, 2114),
                            (2115, 2115),
                            (2116, 2116),
                            (2117, 2117),
                            (2118, 2118),
                            (2119, 2119),
                            (2120, 2120),
                            (2121, 2121),
                            (2122, 2122),
                        ],
                        default=2023,
                        verbose_name="year",
                    ),
                ),
                (
                    "month",
                    models.CharField(
                        choices=[
                            ("January", "January"),
                            ("February", "February"),
                            ("March", "March"),
                            ("April", "April"),
                            ("May", "May"),
                            ("June", "June"),
                            ("July", "July"),
                            ("August", "August"),
                            ("September", "September"),
                            ("October", "October"),
                            ("November", "November"),
                            ("December", "December"),
                        ],
                        default="September",
                        max_length=20,
                        verbose_name="month",
                    ),
                ),
                ("base_brute", models.FloatField(default=2000.0)),
                ("bonus", models.FloatField(default=0.0)),
                ("rappel", models.FloatField(default=0.0)),
                ("n_absences", models.IntegerField(default=0)),
                ("ticket_resto", models.FloatField(default=80.0)),
                ("navigo", models.FloatField(default=42.0)),
                ("extra_bonus", models.FloatField(default=0.0)),
                ("complementaire", models.FloatField(default=56)),
                ("my_net_avant_impot", models.FloatField(blank=True, null=True)),
                (
                    "taux_prelevement",
                    models.DecimalField(decimal_places=2, default=0, max_digits=5),
                ),
                (
                    "taux_prelevement_theorique",
                    models.DecimalField(decimal_places=2, default=10, max_digits=5),
                ),
                ("my_net", models.FloatField(blank=True, null=True)),
                ("my_impots_a_payer", models.FloatField(blank=True, null=True)),
                (
                    "impot_is_paid",
                    models.BooleanField(default=False, verbose_name="Impôt payé"),
                ),
                (
                    "date_updated",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "date_published",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date published"
                    ),
                ),
                ("slug", models.SlugField(blank=True, unique=True)),
                (
                    "author",
                    models.ForeignKey(
                        default=tx_site.current_user.get_current_user,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Liaison",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "element",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="personal.contribution",
                    ),
                ),
                (
                    "salaire",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="personal.salaire",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="contribution",
            name="salaire",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contributions",
                to="personal.salaire",
            ),
        ),
    ]
