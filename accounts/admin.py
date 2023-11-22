from django.contrib import admin
from .models import UserAccount, ExcelFile


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'password', 'website')


admin.site.register(ExcelFile)
