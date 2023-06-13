from django.contrib import admin
from .models import Organization, Site, Area, Equipment, ControlSystem, Unit, ControlModule, DataPoint, \
    Order, ProductionSchedule, ProcessData, Alarm, Event, ManufacturingFacility, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'site')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'area')


@admin.register(ControlSystem)
class ControlSystemAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'control_system')


@admin.register(ControlModule)
class ControlModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')


@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'control_module')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number',)


@admin.register(ProductionSchedule)
class ProductionScheduleAdmin(admin.ModelAdmin):
    list_display = ('number', 'order')


@admin.register(ProcessData)
class ProcessDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'data_point')


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ManufacturingFacility)
class ManufacturingFacilityAdmin(admin.ModelAdmin):
    list_display = ('organization', 'site', 'area', 'equipment', 'control_system', 'unit', 'control_module',
                    'order', 'production_schedule', 'process_data', 'alarm', 'event')
