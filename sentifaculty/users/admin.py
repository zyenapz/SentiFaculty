from django.apps import apps
from django.contrib import admin
from .models import MclUser, Principal, Student, Teacher

from django.contrib.auth.admin import UserAdmin

from .forms import MclUserCreationForm, MclUserChangeForm
from .models import MclUser


class MclUserAdmin(UserAdmin):
    add_form = MclUserCreationForm
    form = MclUserChangeForm
    model = MclUser
    list_display = ["email", "mcl_id", "first_name",
                    "last_name", "is_staff", "is_active", 'user_type']
    list_filter = ["email", "mcl_id", "first_name",
                   "last_name", "is_staff", "is_active", 'user_type']

    fieldsets = (
        ('User Info', {
                # 'fields': ('mcl_id', 'first_name', 'last_name', 'user_type'),
                'fields': ('mcl_id', 'first_name', 'last_name'),
            }
        ),
        ('Account Info', {
                'fields': ('email', 'password')
            }
        ),
        ('Permissions', {
                'fields': ('is_staff', 'is_active')
            }
        )
    )

    add_fieldsets = (
        (
            'User Info', {
                'fields': ('mcl_id', 'first_name', 'last_name', 'user_type'),
            }
        ),
        (
            'Account Info', {
                'fields': ('email', 'password1', 'password2'),
            }
        )
    )

    search_fields = ('email',)
    ordering = ('email',)

class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ['id', 'user', 'section_ID', 'strand_ID', 'year_level', 'faculty_eval']


admin.site.register(MclUser, MclUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher)
admin.site.register(Principal)

# Register your models here.
# feedback_models = apps.get_app_config('users').get_models()

# for model in feedback_models:
#     admin.site.register(model)
