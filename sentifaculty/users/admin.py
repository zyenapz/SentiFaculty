from django.apps import apps
from django.contrib import admin
from .models import MclUser

from django.contrib.auth.admin import UserAdmin

from .forms import MclUserCreationForm, MclUserChangeForm
from .models import MclUser


class MclUserAdmin(UserAdmin):
    add_form = MclUserCreationForm
    form = MclUserChangeForm
    model = MclUser
    list_display = ["email", "mcl_id", "first_name",
                    "last_name", "is_staff", "is_active"]
    list_filter = ["email", "mcl_id", "first_name",
                   "last_name", "is_staff", "is_active"]

    fieldsets = (
        ('Student Info', {
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
        ),
    )

    add_fieldsets = (
        (
            'Student Info', {
                'fields': ('mcl_id', 'first_name', 'last_name'),
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


admin.site.register(MclUser, MclUserAdmin)

# Register your models here.
# feedback_models = apps.get_app_config('users').get_models()

# for model in feedback_models:
#     admin.site.register(model)
