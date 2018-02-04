#!/usr/bin/env python
import os
import sys


def create_log_dir():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(BASE_DIR, "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)


if __name__ == "__main__":

    create_log_dir()

    if os.environ.get("settings") == "test":
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "settings.settings_test")
    elif os.environ.get("settings") == "pro":
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "settings.settings_pro")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
