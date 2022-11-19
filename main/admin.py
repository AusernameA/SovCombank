from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Transfers

User = get_user_model()

admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['phone', 'passport_ID', 'passport_Series', "amount_of_money",
                    "time_registrate", "approved", "banned", 'admin']
    list_filter = ['admin', "time_registrate", "approved", "banned"]
    fieldsets = (
        (None, {'fields': ('phone', 'password',)}),
        ('Personal info', {'fields': ("passport_ID", "passport_Series", )}),
        ('Permissions', {'fields': ("approved", "banned", 'admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', "passport_ID", "passport_Series",
                       "approved", "banned", 'admin')}
        ),
    )
    search_fields = ['phone']
    ordering = ['approved']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.register(Transfers)
