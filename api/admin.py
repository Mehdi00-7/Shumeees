from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Hobby

admin.site.register(Hobby)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ["email"]
