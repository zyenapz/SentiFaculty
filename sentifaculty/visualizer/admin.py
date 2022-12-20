from django.apps import apps
from django.contrib import admin

visualizer_models = apps.get_app_config('visualizer').get_models()

for model in visualizer_models:
    admin.site.register(model)
