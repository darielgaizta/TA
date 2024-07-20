from django.conf import settings
import os

os.makedirs(settings.TABLES_DIR, exist_ok=True)
os.makedirs(settings.RESULT_DIR, exist_ok=True)