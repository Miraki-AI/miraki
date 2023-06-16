import logging
from django.db import models
from miraki.apps.hub_tenant.base.models import UUIDTimeStampedModel, UserRolesUUIDTimeStampedModel, UserProfile
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class ConnectionInfo(UUIDTimeStampedModel):
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    port = models.IntegerField(default=0)
    connection_parameters = models.JSONField(default=dict)
    mqtt_broker = models.CharField(max_length=100, blank=True, null=True)
    mqtt_port = models.IntegerField(default=0)
    mqtt_username = models.CharField(max_length=100, blank=True, null=True)
    mqtt_password = models.CharField(max_length=100, blank=True, null=True)


class ConnectableDevice(UUIDTimeStampedModel):
    connection = models.OneToOneField(ConnectionInfo, on_delete=models.CASCADE, blank=True, null=True)

    def connect(self):
        # Add your logic to establish connection with the device
        pass

    def read_data(self):
        # Add your logic to read data from the device
        pass

    def write_data(self):
        # Add your logic to write data to the device
        pass

    class Meta:
        abstract = True



class Machine(UserRolesUUIDTimeStampedModel):
    PLC = 'PLC'
    CNC = 'CNC'
    ROBOT = 'Robot'
    AGV = 'AGV'
    VISION = 'Vision'
    EDGE_DEVICE = 'Edge Device'

    MACHINE_TYPES = (
        (PLC, 'PLC'),
        (CNC, 'CNC'),
        (ROBOT, 'Robot'),
        (AGV, 'AGV'),
        (VISION, 'Vision'),
        (EDGE_DEVICE, 'Edge Device'),
    )

    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    description = models.TextField()
    installation_date = models.DateField(auto_now_add=True)
    machine_type = models.CharField(max_length=12, choices=MACHINE_TYPES)
    machine_type_model = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def create_machine_instance(self):
        logging.info("Creating machine instance")
        MachineTypeModel = self.machine_type_model.model_class()
        machine_type_model = MachineTypeModel.objects.create(machine=self.id, name=self.name)
        return machine_type_model.id
            
    def save(self, *args, **kwargs):
        if not self.machine_type_model:
            self.machine_type_model = ContentType.objects.get(app_label='hub_tenant', model=self.machine_type.lower())
            self.machine_type_id = self.create_machine_instance()
        super().save(*args, **kwargs)
        
        
class PLC(ConnectableDevice):
    machine = models.UUIDField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    rack = models.IntegerField(default=0)
    slot = models.IntegerField(default=0)
    timeout = models.IntegerField(default=0)
    connection_protocol = models.CharField(max_length=100, blank=True, null=True)
    # tags = models.ManyToManyField(TagTopics, blank=True)
    # Add more PLC-specific attributes based on your needs

class CNC(ConnectableDevice):
    machine = models.UUIDField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    # tags = models.ManyToManyField(TagTopics, blank=True)
    # Add more CNC-specific attributes based on your needs

class Robot(ConnectableDevice):
    machine = models.UUIDField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    # tags = models.ManyToManyField(TagTopics, blank=True)
    # Add Robot-specific attributes

class AGV(ConnectableDevice):
    machine = models.UUIDField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    # tags = models.ManyToManyField(TagTopics, blank=True)
    # Add AGV-specific attributes

class Vision(ConnectableDevice):
    machine = models.UUIDField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    # tags = models.ManyToManyField(TagTopics, blank=True)
    # Add Vision-specific attributes

class EdgeDevice(ConnectableDevice):
    machine = models.UUIDField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    # tags = models.ManyToManyField(TagTopics, blank=True)
    # Add Edge Device-specific attributes
class Process(UserRolesUUIDTimeStampedModel):
    CHOICE_PROCESS_MACHINING = 'PROCESS_MACHINING'
    CHOICE_USER_QA_STATION = 'USER_QA_STATION'
    CHOICE_VISION_STATION = 'VISION_STATION'
    
    CHOICES = (
        (CHOICE_PROCESS_MACHINING, 'Process Or Machining'),
        (CHOICE_USER_QA_STATION, 'User QA Station'),
        (CHOICE_VISION_STATION, 'Vision Station'),
    )
    
    name = models.CharField(max_length=100)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, blank=True, null=True)
    previous_process = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='prev_process_instance')
    next_process = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='next_process_instance')
    process_type = models.CharField(max_length=100, choices=CHOICES, default=CHOICE_PROCESS_MACHINING)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class TagTopics(UserRolesUUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Line(UserRolesUUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    processes = models.ManyToManyField(Process, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Area(UserRolesUUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    lines = models.ManyToManyField(Line, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
 
class Site(UserRolesUUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    areas = models.ManyToManyField(Area, blank=True)
    
    
    def __str__(self):
        return self.name

