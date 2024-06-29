from django.conf import settings
import os

if not os.path.exists(settings.OUT_DIR):
    os.makedirs(settings.OUT_DIR)