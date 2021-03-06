from django.contrib import admin

from .models import User, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',)
    list_filter = ('email', 'username',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
