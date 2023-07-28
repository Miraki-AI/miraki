import uuid
from django.db import models
from datetime import datetime
from django.conf import settings


    

class UUIDTimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True, default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())

    class Meta:
        abstract = True

class UserProfile(UUIDTimeStampedModel):
    name = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=300, unique=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_img', blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    onboarded = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.email}'
    

class UserRolesUUIDTimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True, default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())
    allowed_users = models.ManyToManyField(UserProfile, related_name='%(class)s_admin_users', blank=True)
    admin_users = models.ManyToManyField(UserProfile, related_name='%(class)s_allowed_users', blank=True)
    
    class Meta:
        abstract = True