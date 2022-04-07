#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

os.environ.setdefault('PAYPAL_CLIENT_ID','AffU1WUZRkKgY-fyLFXYHI6L6blqxJLNx6gIYUVpglHpj48OXYq7GHTe38aFKo0bEQgvpIfGP747QmkT')
os.environ.setdefault('PAYPAL_CLIENT_SECRET','EHkJofCdbTGd7s2t441EnQXNqKNDLWWJCS0dYbHO4dU3WCRC_1Id49duJlpuzBnpApTEQlgHxOkckQUj')

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject01.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
