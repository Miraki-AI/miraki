from rest_framework import serializers
from .models import *
from miraki.apps.customers.models import Organization
from miraki.apps.hub_tenant.base.models import UserProfile
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class TagTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagTopics
        fields = '__all__'
class PLCSerializer(serializers.ModelSerializer):
    tags = TagTopicsSerializer(many=True, read_only=True)
    class Meta:
        model = PLC
        fields = '__all__'
class CNCSerializer(serializers.ModelSerializer):
    tags = TagTopicsSerializer(many=True, read_only=True)
    class Meta:
        model = CNC
        fields = '__all__'
        
class RobotSerializer(serializers.ModelSerializer):
    tags = TagTopicsSerializer(many=True, read_only=True)
    class Meta:
        model = Robot
        fields = '__all__'

class VisionSerializer(serializers.ModelSerializer):
    tags = TagTopicsSerializer(many=True, read_only=True)
    class Meta:
        model = Vision
        fields = '__all__'
        
class AGVSerializer(serializers.ModelSerializer):
    tags = TagTopicsSerializer(many=True, read_only=True)
    class Meta:
        model = AGV
        fields = '__all__'

class MachineTypeModelSerializer(serializers.ModelSerializer):
    machine_type_model = serializers.SerializerMethodField()

    def get_machine_type_model(self, obj):
        machine_type_model = obj.machine_type_model.model_class()
        machine_type = obj.machine_type
        obj = machine_type_model.objects.filter(machine=obj.id)
        serializer_class = None

        if machine_type == 'PLC':
            serializer_class = PLCSerializer
        elif machine_type == 'CNC':
            serializer_class = CNCSerializer
        elif machine_type == 'Robot':
            serializer_class = RobotSerializer
        elif machine_type == 'Vision':
            serializer_class = VisionSerializer
        elif machine_type == 'AGV':
            serializer_class = AGVSerializer
            

        if serializer_class:
            serializer = serializer_class(obj, many=True)
            logging.info("machines", serializer.data)
            return serializer.data

        return None
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     return representation.pop('machine_type_model', None)
    
    class Meta:
        model = Machine
        fields = "__all__"

class MachineSerializer(serializers.ModelSerializer):
    machine_type_model = serializers.SerializerMethodField()
    
    def get_machine_type_model(self, obj):
        return MachineTypeModelSerializer(obj).data
    class Meta:
        model = Machine
        fields = '__all__'

class ProcessSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    machine = MachineSerializer()
    
    def get_tags(self, obj):
        return TagTopicsSerializer(TagTopics.objects.filter(process=obj.id), many=True).data
    class Meta:
        model = Process
        fields = '__all__'
class LineSerializer(serializers.ModelSerializer):
    processes = ProcessSerializer(many=True, read_only=True)
    class Meta:
        model = Line
        fields = '__all__'
        
class AreaSerializer(serializers.ModelSerializer):
    lines = LineSerializer(many=True, read_only=True)
    class Meta:
        model = Area
        fields = '__all__'


class SiteSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True, read_only=True)
    class Meta:
        model = Site
        fields = '__all__'







class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        


class MyDashboardSerializer(serializers.ModelSerializer):
    created_by = UserProfileSerializer()
    class Meta:
        model = MyDashboard
        fields = ('id', 'name', 'created_by', 'widgets', 'is_default')