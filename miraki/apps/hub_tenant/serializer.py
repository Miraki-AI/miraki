from rest_framework import serializers
from .models import Organization, Site, Area, Equipment, ControlSystem, Unit, ControlModule, DataPoint, \
    Order, ProductionSchedule, ProcessData, Alarm, Event, ManufacturingFacility, UserProfile


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'


class ControlSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlSystem
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class ControlModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlModule
        fields = '__all__'


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ProductionScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionSchedule
        fields = '__all__'


class ProcessDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessData
        fields = '__all__'


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class ManufacturingFacilitySerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    site = SiteSerializer(many=True)
    area = AreaSerializer(many=True)
    equipment = EquipmentSerializer(many=True)
    control_system = ControlSystemSerializer(many=True)
    unit = UnitSerializer()
    control_module = ControlModuleSerializer()
    order = OrderSerializer(many=True)
    production_schedule = ProductionScheduleSerializer(many=True)
    process_data = ProcessDataSerializer(many=True)
    alarm = AlarmSerializer(many=True)
    event = EventSerializer(many=True)

    class Meta:
        model = ManufacturingFacility
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'is_admin','is_active', 'email')