from django.contrib import admin

from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'user_name','contact_no')
    list_filter = ('email', 'user_name', 'is_active', 'is_staff')
    ordering = ('created_date',)
    list_display = ('email', 'is_editable',
                    'is_active', 'is_staff', )
    fieldsets = (
        (None, {'fields': ('email','password',  'user_name', 'contact_no', 'created_by', 'status', 'is_editable')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',  'is_moderator', 'is_owner', 'is_employee','groups')}),
        
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'user_name', 'created_by', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )



admin.site.register(User, UserAdminConfig)