from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserAdmin(admin.UserAdmin):
    pass


admin.site.register(User, CustomUserAdmin)
