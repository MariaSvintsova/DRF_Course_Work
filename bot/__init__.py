import os

import django



# Установите модуль настроек для Django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')



# Настройте Django

django.setup()