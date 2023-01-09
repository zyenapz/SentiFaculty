from django.apps import apps
from django.contrib import admin

# Register your models here.
feedback_models = apps.get_app_config('users').get_models()

for model in feedback_models:
    admin.site.register(model)