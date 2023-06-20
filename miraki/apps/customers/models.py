from django.db import models

from miraki.apps.hub_tenant.base.models import UUIDTimeStampedModel

class Licence(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)
    is_expired = models.BooleanField(default=False)
    is_trial = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    sites_allowed = models.IntegerField(default=0)
    areas_allowed = models.IntegerField(default=0)
    lines_allowed = models.IntegerField(default=0)
    tags_allowed = models.IntegerField(default=0)
    users_allowed = models.IntegerField(default=0)
    def __str__(self):
        return self.name
class Organization(UUIDTimeStampedModel):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)
    # created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    license = models.OneToOneField(Licence, on_delete=models.CASCADE, blank=True, null=True)
    # default true, schema will be automatically created and synced when it is saved
    
    def __str__(self):
        return self.name
