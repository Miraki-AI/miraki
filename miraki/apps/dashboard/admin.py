from django.contrib import admin

from miraki.apps.dashboard.models import Dashboard


class DashboardAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")

admin.site.register(Dashboard, DashboardAdmin)