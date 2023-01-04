from django.apps import apps
from django.contrib import admin

feedback_models = apps.get_app_config('feedback').get_models()

for model in feedback_models:
    admin.site.register(model)
