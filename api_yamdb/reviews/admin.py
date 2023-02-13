from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'first_name',
                    'last_name',
                    'bio',
                    'role',
                    'is_staff',
                    'is_superuser',
                    )


admin.site.register(User, UserAdmin)
