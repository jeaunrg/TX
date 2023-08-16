#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import glob
import os
import shutil
import subprocess
import sys

from tx_site.settings import BASE_DIR, DATABASES

MANAGE_CMD = ["python", BASE_DIR / "manage.py"]


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tx_site.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def clear():
    # delete migrations
    for migration_file in BASE_DIR.glob("*/migrations/*.py"):
        if migration_file.name != "__init__.py":
            migration_file.unlink()

    # delete database
    db_path = DATABASES["default"]["NAME"]
    db_path.unlink(missing_ok=True)

    # delete media
    media_path = BASE_DIR / "media_cdn"
    media_path.rmdir()
    media_path.mkdir()


def init():
    subprocess.run(MANAGE_CMD + ["makemigrations"])
    subprocess.run(MANAGE_CMD + ["migrate"])

    # create superuser
    os.environ["DJANGO_SUPERUSER_PASSWORD"] = "admin"
    subprocess.run(
        MANAGE_CMD
        + [
            "createsuperuser",
            "--noinput",
            "--username",
            "admin",
            "--email",
            "admin@gmail.com",
        ]
    )


if __name__ == "__main__":
    if "--reset" in sys.argv:
        clear()
        init()
        sys.argv.remove("--reset")
    main()
