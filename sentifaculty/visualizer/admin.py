from django.apps import apps
from django.contrib import admin

from visualizer.models import AcademicYear, FacultyEvaluation, Section, Strand, Subject, YearLevel

# Admin classes
class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    list_display = [field.name for field in Subject._meta.get_fields()]

# Register models
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Section)
admin.site.register(Strand)
admin.site.register(AcademicYear)
admin.site.register(YearLevel)
admin.site.register(FacultyEvaluation)

# # Register everything else
# visualizer_models = apps.get_app_config('visualizer').get_models(e)

# for model in visualizer_models:
#     admin.site.register(model)
