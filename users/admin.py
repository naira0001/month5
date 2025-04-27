from django.contrib import admin
from django.contrib.auth.models import User
from .models import SMSCode

# Регистрация модели SMSCode
@admin.register(SMSCode)
class SMSCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')  # Поля, которые будут отображаться в списке
    search_fields = ('user__username', 'code')  # Поля для поиска