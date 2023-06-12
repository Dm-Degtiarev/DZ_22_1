from django.contrib import admin
from user.models import User


@admin.register(User)
class UserAdmib(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
