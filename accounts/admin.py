from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # id가 없으면 자동으로 생성됨
    list_display = ['id', 'nickname', 'user']
    list_display_links = ['nickname', 'user']
    search_fields = ['nickname']
