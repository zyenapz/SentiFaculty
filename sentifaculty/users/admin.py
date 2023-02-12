from django.apps import apps
from django.contrib import admin
from .models import MalayanUser, Student, Teacher

from django.contrib.auth.admin import UserAdmin

from .forms import MalayanUserCreationForm, MalayanUserChangeForm
from .models import MalayanUser

@admin.register(MalayanUser)
class MalayanUserAdmin(UserAdmin):
    add_form = MalayanUserCreationForm
    form = MalayanUserChangeForm
    model = MalayanUser
    list_display = ["email", "mcl_id", "first_name",
                    "last_name", "is_staff", "is_active", 'user_type']
    list_filter = ["email", "mcl_id", "first_name",
                   "last_name", "is_staff", "is_active", 'user_type']

    fieldsets = (
        ('User Info', {
                # 'fields': ('mcl_id', 'first_name', 'last_name', 'user_type'),
                'fields': ('mcl_id', 'first_name', 'last_name', 'user_type'),
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
    list_display = ['id', 'user', 'section', 'strand', 'year_level']
    filter_horizontal = ['subjects',]

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher)
# admin.site.register(Principal)

# Register your models here.
# feedback_models = apps.get_app_config('users').get_models()

# for model in feedback_models:
#     admin.site.register(model)
