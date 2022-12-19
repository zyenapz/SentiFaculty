from django.apps import AppConfig


class VisualizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visualizer'

    def ready(self):
        # NOTE vscode might give a warning about failed imports,
        # this a certified michaelsoft (pylance) moment
        import visualizer.signals
