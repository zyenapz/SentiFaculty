from django.apps import apps
from django.contrib import admin

from visualizer.models import AcademicYear, FacultyEvaluation, Section, Strand, Subject, YearLevel

# Admin classes
class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    list_display = ['id', 'subject_code', 'subject_name']

# Register models
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Section)
admin.site.register(Strand)
admin.site.register(AcademicYear)
admin.site.register(YearLevel)
admin.site.register(FacultyEvaluation)
admin.site.site_url = "/visualizer/admin-home"
admin.site.index_title = "FE Management"
admin.site.site_header = "Faculty Evaluation Management"

# # Register everything else
# visualizer_models = apps.get_app_config('visualizer').get_models(e)

# for model in visualizer_models:
#     admin.site.register(model)
