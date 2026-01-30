from django.contrib import admin
from .models import WebRegistration, WebTeammember

class WebTeammemberInline(admin.TabularInline):
    model = WebTeammember
    extra = 0

@admin.register(WebRegistration)
class WebRegistrationAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'team_leader_name', 'created_at')
    inlines = [WebTeammemberInline]
