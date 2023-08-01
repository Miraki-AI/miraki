from miraki.apps.hub_tenant.models import *
from django.db.models import Q

class Permissions:
    def __init__(self, userprofile, object=None):
        self.userprofile = userprofile
        self.object = object
        self.permissions = {}

    def is_super_admin(self):
        return self.userprofile.is_admin
    
    def is_allowed(self):
        try:
            if self.userprofile in self.object.allowed_users.all():
                return True
            else:
                return False
        except Exception as e:
            raise e
        
    def is_admin(self):
        try:
            if self.userprofile in self.object.admin_users.all():
                return True
            else:
                return False
        except Exception as e:
            raise e
        
    def fetch_permissions(self):
        if self.is_super_admin():
            self.permissions['is_allowed'] = True
            self.permissions['is_admin'] = True
            self.permissions['is_super_admin'] = True
        elif self.is_allowed():
            self.permissions['is_allowed'] = True
            self.permissions['is_admin'] = False
            self.permissions['is_super_admin'] = False
        elif self.is_admin():
            self.permissions['is_allowed'] = False
            self.permissions['is_admin'] = True
            self.permissions['is_super_admin'] = False
        else:
            self.permissions['is_allowed'] = False
            self.permissions['is_admin'] = False
            self.permissions['is_super_admin'] = False
        return self.permissions
    
    
    def fetch_all_permitted(self, entityModel):
        if self.is_super_admin():
            return entityModel.objects.all()
        else:
            return entityModel.objects.filter(Q(allowed_users=self.userprofile) | Q(admin_users=self.userprofile))
        
    
