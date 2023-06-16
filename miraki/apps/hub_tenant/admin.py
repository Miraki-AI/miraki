from django.contrib import admin
from .models import *
from miraki.apps.customers.models import Organization
from miraki.apps.hub_tenant.base.models import UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['id']



@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['id']



@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ['id']

    
@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ['id']

    

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['id']

    
    
@admin.register(PLC)
class PLCAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(CNC)
class CNCAdmin(admin.ModelAdmin):
    list_display = ['id']

    
@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ['id']

    
@admin.register(Vision)
class VisionAdmin(admin.ModelAdmin):
    list_display = ['id']

    
@admin.register(AGV)
class AGVAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(TagTopics)
class TagTopicsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']