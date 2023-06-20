from miraki.apps.hub_tenant.models import *
from django.db.models import Q

class Permissions:
    def __init__(self, userprofile):
        self.userprofile = userprofile
        self.permissions = []

    def get_permissions(self):
        self.permissions = []
        # self.permissions.extend(self.get_user_permissions())
        # self.permissions.extend(self.get_organization_permissions())
        self.permissions.extend(self.get_site_permissions())
        # self.permissions.extend(self.get_module_permissions())
        return self.permissions

    def get_user_permissions(self):
        return [
            "hub.userprofile.add_userprofile",
            "hub.userprofile.change_userprofile",
            "hub.userprofile.delete_userprofile",
            "hub.userprofile.view_userprofile",
        ]

    def get_organization_permissions(self):
        return [
            "hub.organization.add_organization",
            "hub.organization.change_organization",
            "hub.organization.delete_organization",
            "hub.organization.view_organization",
        ]

    def get_site_permissions(self, site_id):
        site_permissions = []
        logging.info(f"User: {self.userprofile}")
        # if site := Site.objects.filter(allowed_users__in=[self.userprofile]).filter(
        #    Q(id=site_id)
        # ):
        #     site_permissions.extend(
        #         [
        #         "hub.site.view_site",
        #         ]
        #     )
        
        if site := Site.objects.get(
            Q(id=site_id) and Q(admin_users__in=[self.userprofile])
        ):
            site_permissions.extend(
                [
                    "hub.site.add_site",
                    "hub.site.change_site",
                    "hub.site.delete_site",
                ]
            )
        
        return site_permissions

    def get_module_permissions(self):
        return [
            "hub.module.add_module",
            "hub.module.change_module",
            "hub.module.delete_module",
            "hub.module.view_module",
        ]
