from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_verified',
                    'is_active', 'is_staff', 'is_superuser']
    list_filter = ['email', 'is_staff', 'is_superuser', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_verified', 'is_staff', 'is_active', 'is_superuser',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    class Meta:
        model = User


admin.site.register(User, CustomUserAdmin)
