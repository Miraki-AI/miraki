import logging

from django.contrib.auth import get_user_model

from miraki.apps.hub_tenant.models import *
from miraki.apps.hub_tenant.base.models import UserProfile
from miraki.apps.hub_tenant.serializer import *

User = get_user_model()
class UserOnBoard:
    def __init__(self, request):
        self.data = request.data
        self.tenant = request.tenant
        self.profile_image = request.FILES.get('profile_image')
        logging.info(f"User onboarding request: {self.data}")
        
    def onboard_user(self):
        try:
            if self.is_user_exists():
                raise Exception('User already exists')
            if user := self.create_user():
                self.create_userprofile(user)
                return True
        except Exception as e:
            raise Exception(str(e))
    
    def create_user(self):
        try:
            user = User()
            user.email = self.data['email']
            user.set_password(self.data['password'])
            user.save()
            return user
        except Exception as e:
            raise Exception(f'Error in Creating User - {str(e)}')
    
    def create_userprofile(self, user):
        try:
            userprofile = UserProfile()
            userprofile.name = self.data['name']
            userprofile.email = self.data['email']
            userprofile.mobile = self.data['mobile']
            userprofile.profile_img = self.profile_image
            userprofile.user = user
            userprofile.is_active = True
            if self.data['org_admin'] == 'true':
                userprofile.is_admin = True
            userprofile.save()
        except Exception as e:
            raise Exception(f'Error in Creating User Profile{str(e)}')
    
    def is_user_exists(self):
        try:
            User.objects.get(email=self.data['email'])
            return True
        except Exception as e:
            return False
    
    def send_email(self):
        pass
    

class ManageSite:
    def __init__(self, request=None):
        self.data = request.data
        self.tenant = request.tenant
        self.request = request
        logging.info(f"Manage Site request: {self.data}")
    
    def __get_user(self):
        return UserProfile.objects.get(user=self.request.user)
    
    def get_site_instance_by_id(self, site_id):
        try:
            return Site.objects.get(id=site_id)
        except Exception as e:
            raise Exception(f'Error in getting site by id - {str(e)}')
    
    def create_site(self):
        try:
            site = Site(
                name=self.data['name'],
                address=self.request.data['address'],
                state=self.request.data['state'],
                zipcode=self.request.data['zipcode'],
                country=self.request.data['country'],
                created_by=self.__get_user()
                
            )
            site.save()
            
            if self.data.get('areas', None):
                for area in self.data['areas']:
                    site.areas.add(area)
            
            if self.data.get('allowed_users', None):
                for user in self.data['allowed_users']:
                    site.allowed_users.add(user)
            if self.data.get('admin_users', None):
                for user in self.data['admin_users']:
                    site.admin_users.add(user)
                    
            serializer = SiteSerializer(site)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in creating site - {str(e)}')
    
    def delete_site(self, instance):
        try:
            #check_permissions
            instance.delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting site - {str(e)}')
    
    def update_area(self, areas, id=None):
        try:
            if id:
                site = self.get_site_instance_by_id(id)
                for area in areas:
                    print(area, type(area))
                    site.areas.add(area)
                site.save()
            else:
                #TODO: flexibility to get called from create_site()
                pass
        except Exception as e:
            raise Exception(f'Error in updating area - {str(e)}')
                    
            
        
        
        
class ManageArea:
    def __init__(self, request=None):
        self.data = request.data
        self.tenant = request.tenant
        self.request = request
        logging.info(f"Manage Area request: {self.data}")
    
    def __get_user(self):
        return UserProfile.objects.get(user=self.request.user)
    
    def get_area_instance_by_id(self, area_id):
        try:
            return Area.objects.get(id=area_id)
        except Exception as e:
            raise Exception(f'Error in getting area by id - {str(e)}')
    
    def create_area(self):
        try:
            area = Area(
                name=self.data['name'],
                created_by=self.__get_user()
            )
            
            area.save()
            if self.data.get('allowed_users', None):
                for user in self.data['allowed_users']:
                    area.allowed_users.add(user)
            if self.data.get('admin_users', None):
                for user in self.data['admin_users']:
                    area.admin_users.add(user)
            
            area.save()
                    
            serializer = AreaSerializer(area)
            
            #Map this area to site requested for creation
            self._map_area_to_site(str(area.id))
            
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in creating area - {str(e)}')
    
    def delete_area(self, instance):
        try:
            #check_permissions
            instance.delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting area - {str(e)}')
    
    def _map_area_to_site(self,area):
        try:
            ManageSite(self.request).update_area([area],id=self.data['site'])
        except Exception as e:
            raise Exception(f'Error in mapping area to site - {str(e)}')
    
    def update_lines(self, lines, id=None):
        try:
            if id:
                area = self.get_area_instance_by_id(id)
                for line in lines:
                    area.lines.add(line)
                area.save()
            else:
                #TODO: flexibility to get called from create_area()
                pass
        except Exception as e:
            raise Exception(f'Error in updating lines - {str(e)}')        
        

class ManageLine:
    def __init__(self, request):
        self.data = request.data
        self.tenant = request.tenant
        self.request = request
        logging.info(f"Manage Line request: {self.data}")
    
    def __get_user(self):
        return UserProfile.objects.get(user=self.request.user)
    
    def get_line_instance_by_id(self, line_id):
        try:
            return Line.objects.get(id=line_id)
        except Exception as e:
            raise Exception(f'Error in getting line by id - {str(e)}')
    
    def create_line(self):
        try:
            line = Line(
                name=self.data['name'],
                created_by=self.__get_user()
            )
            
            line.save()
            if self.data.get('allowed_users', None):
                for user in self.data['allowed_users']:
                    line.allowed_users.add(user)
            if self.data.get('admin_users', None):
                for user in self.data['admin_users']:
                    line.admin_users.add(user)
            
            line.save()
            serializer = LineSerializer(line)
            #Map this area to site requested for creation
            self._map_line_to_area(str(line.id))
            
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in creating line - {str(e)}')
    
    def delete_line(self, instance):
        try:
            #check_permissions
            instance.delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting line - {str(e)}')
    
    def _map_line_to_area(self,line):
        try:
            ManageArea(self.request).update_lines([line],id=self.data['area'])
        except Exception as e:
            raise Exception(f'Error in mapping line to area - {str(e)}')
        
    def update_processes(self, processes, id=None):
        try:
            if id:
                line = self.get_line_instance_by_id(id)
                for process in processes:
                    line.processes.add(Process.objects.get(id=process))
                line.save()
            else:
                #TODO: flexibility to get called from create_line()
                pass
        except Exception as e:
            raise Exception(f'Error in updating processes - {str(e)}')
        
        
class ManageProcess:
    def __init__(self, request):
        self.request = request
        self.data = request.data
        self.tenant = request.tenant
        
        logging.info(f"Manage Process request: {self.data}")
    
    def __get_user(self):
        return UserProfile.objects.get(user=self.request.user)
    
    def get_process_instance_by_id(self, process_id):
        try:
            return Process.objects.get(id=process_id)
        except Exception as e:
            raise Exception(f'Error in getting process by id - {str(e)}')
        
    def create_process(self):
        try:
            process = Process(
                name=self.data['name'],
                created_by=self.__get_user()
            )
            
            process.save()
            if self.data.get('allowed_users', None):
                for user in self.data['allowed_users']:
                    process.allowed_users.add(user)
            if self.data.get('admin_users', None):
                for user in self.data['admin_users']:
                    process.admin_users.add(user)
            
            process.save()
            serializer = ProcessSerializer(process)
            #Map this area to site requested for creation
            self._map_process_to_line(str(process.id))
            
            return serializer.data
        except Exception as e:
            logging.error(f'Error in creating process - {str(e)}')
            raise Exception(f'Error in creating process - {str(e)}')
        
    def delete_process(self, instance):
        try:
            #check_permissions
            instance.delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting process - {str(e)}')
        
    
    def _map_process_to_line(self,process):
        try:
            ManageLine(self.request).update_processes([process],id=self.data['line'])
        except Exception as e:
            raise Exception(f'Error in mapping process to line - {str(e)}')
        
    def update_machine(self, machine, id=None):
        try:
            if id:
                logging.info(f"Updating machine for process {id} with machine {machine}")
                process = self.get_process_instance_by_id(id)
                process.machine = Machine.objects.get(id=machine)
                process.save()
            else:
                pass
        except Exception as e:
            raise Exception(f'Error in updating machines - {str(e)}')
        
class ManageMachine:
    def __init__(self, request):
        self.request = request
        self.data = request.data
        self.tenant = request.tenant
        
        logging.info(f"Manage Machine request: {self.data}")
        
    def __get_user(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except Exception as e:
            raise Exception(f'Error in getting user - {str(e)}')
        
    def get_machine_instance_by_id(self, machine_id):
        try:
            return Machine.objects.get(id=machine_id)
        except Exception as e:
            raise Exception(f'Error in getting machine by id - {str(e)}')
        
    def create_machine(self):
        try:
            machine = Machine(
                name=self.data['name'],
                machine_type=self.data['machine_type'],
                manufacturer=self.data['manufacturer'],
                model_number=self.data['model_number'],
                serial_number=self.data['serial_number'],
                is_active=True,
                created_by=self.__get_user()
            )
            
            # if self.data.get('allowed_users', None):
            #     for user in self.data['allowed_users']:
            #         logging.info(f"Allowed user: {user} type: {type(user)}")
            #         machine.allowed_users.set(UserProfile.objects.get(id=user))
            # if self.data.get('admin_users', None):
            #     for user in self.data['admin_users']:
            #         machine.admin_users.set(user)
            
            machine.save()
            self._map_machine_to_process(str(machine.id), self.data['process'])
            serializer = MachineSerializer(machine)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in creating machine - {str(e)}')
    
    def delete_machine(self, instance):
        try:
            #check_permissions
            instance.delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting machine - {str(e)}')
        
    def _map_machine_to_process(self,machine, process):
        try:
            ManageProcess(self.request).update_machine(machine, id=process)
        except Exception as e:
            raise Exception(f'Error in mapping machine to process - {str(e)}')
        
    def update_machine(self, machine, id=None):
        try:
            if id:
                machine = self.get_machine_instance_by_id(id)
                machine.save()
            else:
                pass
        except Exception as e:
            raise Exception(f'Error in updating machines - {str(e)}')
        