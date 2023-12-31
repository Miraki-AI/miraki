from django import forms
from miraki.apps.hub_tenant.models import *

class InviteUserForm(forms.Form):
    email = forms.EmailField()
    
class UserProfileUpdateForm(forms.Form):
    id = forms.UUIDField()
    name = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=100)
    profile_image = forms.ImageField(required=False)
    password = forms.CharField(max_length=100, required=False)
    
    
    
    
class UserOnboardForm(forms.Form):
    id = forms.UUIDField()
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=100)
    profile_image = forms.ImageField(required=False)
    password = forms.CharField(max_length=100)
    org_admin = forms.BooleanField(required=False)
    

class ConnectionInfoForm(forms.Form):
    ip_address = forms.CharField(max_length=100)
    port = forms.IntegerField()
    connection_parameters = forms.CharField(max_length=100)
    mqtt_broker = forms.CharField(max_length=100)
    mqtt_port = forms.IntegerField()
    mqtt_username = forms.CharField(max_length=100)
    mqtt_password = forms.CharField(max_length=100)

class MachineForm(forms.Form):
    name = forms.CharField(max_length=100)
    manufacturer = forms.CharField(max_length=100)
    model_number = forms.CharField(max_length=100)
    serial_number = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    machine_type = forms.CharField(max_length=100)
    is_active = forms.BooleanField()
    admin_users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())
    allowed_users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())
    process = forms.UUIDField()

class PLCForm(forms.Form):
    name = forms.CharField(max_length=100)
    machine = forms.ModelChoiceField(queryset=Machine.objects.all())
    plc_type = forms.CharField(max_length=100)
    rack = forms.IntegerField()
    slot = forms.IntegerField()
    connection_protocol = forms.CharField(max_length=100)


class CNCForm(forms.Form):
    name = forms.CharField(max_length=100)
    machine = forms.ModelChoiceField(queryset=Machine.objects.all())

class RobotForm(forms.Form):
    name = forms.CharField(max_length=100)
    machine = forms.ModelChoiceField(queryset=Machine.objects.all())


class AGVForm(forms.Form):
    name = forms.CharField(max_length=100)
    machine = forms.ModelChoiceField(queryset=Machine.objects.all())


class VisionForm(forms.Form):
    name = forms.CharField(max_length=100)
    machine = forms.ModelChoiceField(queryset=Machine.objects.all())


class EdgeDeviceForm(forms.Form):
    name = forms.CharField(max_length=100)
    machine = forms.ModelChoiceField(queryset=Machine.objects.all())





class TagTopicsForm(forms.Form):
    name = forms.CharField(max_length=100)
    topic = forms.CharField(max_length=100)
    value = forms.CharField(max_length=100)


class ProcessForm(forms.Form):
    name = forms.CharField(max_length=100)
    machine = forms.ModelChoiceField(queryset=Machine.objects.all(), required=False)
    previous_process = forms.ModelChoiceField(queryset=Process.objects.all(), required=False)
    next_process = forms.ModelChoiceField(queryset=Process.objects.all(), required=False)
    process_type = forms.CharField(max_length=100)
    admin_users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())
    allowed_users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())
    line = forms.UUIDField()    

class LineForm(forms.Form):
    name = forms.CharField(max_length=100)
    processes = forms.ModelMultipleChoiceField(queryset=Process.objects.all(), required=False)
    admin_users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())
    allowed_users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())
    area = forms.UUIDField()


class AreaForm(forms.Form):
    name = forms.CharField(max_length=100)
    site = forms.UUIDField()
    lines = forms.ModelMultipleChoiceField(queryset=Line.objects.all(), required=False)
    allowed_users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())
    admin_users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())


class SiteForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zipcode = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    areas = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=False)
    allowed_users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())
    admin_users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())