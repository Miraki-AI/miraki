from django.db import models
from miraki.apps.customers.models import Organization
from miraki.apps.hub_tenant.base.models import UUIDTimeStampedModel
from django.conf import settings

class UserProfile(UUIDTimeStampedModel):
    name = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=300, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class Site(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Area(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Equipment(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ControlSystem(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Unit(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    control_system = models.ForeignKey(ControlSystem, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ControlModule(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DataPoint(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    control_module = models.ForeignKey(ControlModule, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(UUIDTimeStampedModel):
    number = models.CharField(max_length=100)

    def __str__(self):
        return self.number


class ProductionSchedule(UUIDTimeStampedModel):
    number = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.number


class ProcessData(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    data_point = models.ForeignKey(DataPoint, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Alarm(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Event(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ManufacturingFacility(UUIDTimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    control_system = models.ForeignKey(ControlSystem, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    control_module = models.ForeignKey(ControlModule, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    production_schedule = models.ForeignKey(ProductionSchedule, on_delete=models.CASCADE)
    process_data = models.ForeignKey(ProcessData, on_delete=models.CASCADE)
    alarm = models.ForeignKey(Alarm, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Facility: {self.organization} - {self.site} - {self.area} - {self.equipment}"
    
    

