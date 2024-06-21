from django import setup
import os

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    setup()