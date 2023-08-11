import logging

from django.conf import settings
from django.contrib.auth import get_user_model

from miraki.apps.hub_tenant.models import *
from miraki.apps.hub_tenant.base.models import UserProfile
from miraki.apps.hub_tenant.serializer import *
from miraki.apps.hub_tenant.permissions import Permissions
from miraki.apps.hub_tenant.forms import *
from django.core.mail import send_mail
User = get_user_model()
class FetchPermissions:
    def __init__(self,userprofile):
        self.userprofile = userprofile
        self.permissions = Permissions(self.userprofile)
    
    def get_permissions(self, object=None):
        try:
            if object:
                return Permissions(self.userprofile, object).fetch_permissions()
            else:
                return Permissions(self.userprofile).fetch_permissions()
        except Exception as e:
            raise Exception(f'Error in getting permissions - {str(e)}')
        

class ManageUser:
    def __init__(self, request=None):
        if request:
            self.data = request.data
            self.profile_image = request.FILES.get('profile_image' , None)
        
    def onboard_user(self):
        try:
            userprofile = UserProfile.objects.get(id=self.data['id'])
            if userprofile.onboarded:
                raise Exception('User Already Onboarded')
            userprofile.name = self.data.get('name', None)
            userprofile.mobile = self.data.get('mobile', None)
            if self.profile_image:
                userprofile.profile_img = self.profile_image
            user_instance = userprofile.user
            user_instance.set_password(self.data['password'])
            user_instance.save()
            userprofile.onboarded = True
            userprofile.save()
        
        except Exception as e:
            raise Exception(str(e))
    
    def create_user(self):
        try:
            user = User()
            user.email = self.data['email']
            user.save()
            return user
        except Exception as e:
            raise Exception(f'Error in Creating User - {str(e)}')
    
    def create_userprofile(self, user):
        try:
            userprofile = UserProfile()
            userprofile.name = self.data.get('name', None)
            userprofile.email = self.data.get('email', None)
            userprofile.mobile = self.data.get('mobile', None)
            userprofile.profile_img = self.profile_image
            userprofile.user = user
            userprofile.is_active = True
            if self.data['org_admin'] == 'true':
                userprofile.is_admin = True
            userprofile.save()
            return userprofile
        except Exception as e:
            raise Exception(f'Error in Creating User Profile{str(e)}')
    
    def update_userprofile(self):
        try:
            if not UserProfileUpdateForm(self.data).is_valid():
                raise Exception(UserProfileUpdateForm(self.data).errors)
            userprofile = UserProfile.objects.get(id=self.data['id'])
            userprofile.name = self.data.get('name', None)
            userprofile.mobile = self.data.get('mobile', None)
            userprofile.profile_img = self.profile_image
            userprofile.is_active = True
            userprofile.save()
            if self.data.get('password', None):
                userprofile.user.set_password(self.data['password'])
                userprofile.user.save()
            return UserProfileSerializer(userprofile).data
        except Exception as e:
            raise Exception(f'Error in Updating User Profile{str(e)}')
        
    
    def invite_userprofile(self, user):
        try:
            userprofile = UserProfile()
            if self.data.get('email', None):
                userprofile.email = self.data.get('email', None)
                userprofile.user = user
                userprofile.save()
            return userprofile
        except Exception as e:
            raise Exception(f'Error in Creating User Profile{str(e)}')
    
    def is_user_exists(self, email=None):
        try:
            if email:
                user = User.objects.get(email=email)
            else:
                user = User.objects.get(email=self.data['email'])
            return True
        except Exception as e:
            return False
    
    def send_email(self, email):
        try:
            send_mail(
            email['subject'],  # subject
            email['message'],  # message
            "vijenderpanda@miraki.ai" , # from email
            email['to_emails'],  # to email
            fail_silently=False,
        )
        except Exception as e:
            logging.error(f"Error in sending email - {str(e)}")
            pass
        
    
    def invite_user(self):
        try:
            if self.is_user_exists():
                raise Exception('User already exists')
            if user := self.create_user():
                userprofile = self.invite_userprofile(user)
                return self.send_invite_email(userprofile)
        except Exception as e:
            raise Exception(
                f'Error in inviting user - {str(e)}'
            )
    
    def send_invite_email(self, userprofile):
        try:
            invite_link = f"http://{settings.SUBDOMAIN}/miraki.ai/invite/{userprofile.id}?email={userprofile.email}"
            logging.info(f"Invite link: {invite_link}")
            email = dict(
                subject='Invitation to Miraki',
                message = f"Hi {userprofile.name},\n\nYou have been invited to Miraki. Please click on the link below to complete your registration.\n\n{invite_link}\n\nThanks,\nMiraki Team",
                to_emails = [
                    'vijenderpanda@miraki.ai',
                    'sarthakkapoor@miraki.ai',
                    'ajaisrivastava@miraki.ai',
                    'bharteshsingh@miraki.ai',
                    'vijender.in@gmail.com'
                ]
            )
            self.send_email(email)
            return invite_link
        except Exception as e:
            logging.error(f"Error in sending invite email - {str(e)}")
            raise Exception(f'Error in sending invite email - {str(e)}')
    
    def get_user_profile(self, user_id=None):
        try:
            userprofile = UserProfile.objects.get(id=user_id)
            userprofile = UserProfileSerializer(userprofile).data
            return userprofile
        except Exception as e:
            raise Exception(f'Error in getting user - {str(e)}')
    

class ManageSite(FetchPermissions):
    def __init__(self, request=None):
        self.data = request.data
        self.request = request
        self.userprofile = self.__get_user()
        logging.info(f"Manage Site request: {self.data}")
        super().__init__(self.userprofile)
        
    
    def __get_user(self):
        return UserProfile.objects.get(user=self.request.user)
    
    def get_site_instance_by_id(self, site_id):
        try:
            return Site.objects.get(id=site_id)
        except Exception as e:
            raise Exception(f'Error in getting site by id - {str(e)}')
    
    def get_site(self, pk=None):
        try:
            if pk:
                site = self.get_site_instance_by_id(pk)
                permissions = self.get_permissions(site)
                if (
                    permissions['is_allowed'] or 
                    permissions['is_admin'] or 
                    permissions['is_super_admin']
                ):
                    serializer = SiteSerializer(site)
                else:
                    raise Exception('User not allowed to access this site')
            else:
                # GetAll Sites by User Permission Levels
                sites = self.permissions.fetch_all_permitted(Site)
                print(sites)
                serializer = SiteSerializer(sites, many=True)
            
            try:
                data = serializer.data
            except:
                data = serializer.data
            return data
        except Exception as e:
            raise Exception(f'Error in getting site - {str(e)}')

    
    def create_site(self):
        try:
            permissions = self.permissions.get_site_permissions()
            logging.info(f"Permissions: {permissions}")
        except :
            pass
             
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
        
    def update_site(self, instance):
        logging.info("Updating site")
        try:
            site = instance
            site.name = self.data['name']
            site.address = self.data['address']
            site.state = self.data['state']
            site.zipcode = self.data['zipcode']
            site.country = self.data['country']
            
            logging.info(site)
            
            
            if self.data.get('areas', None):
                for area in self.data['areas']:
                    site.areas.add(area)
            
            if self.data.get('allowed_users', None):
                site.allowed_users.clear()
                for user in self.data['allowed_users']:
                    site.allowed_users.add(UserProfile.objects.get(id=user))
                    
            if self.data.get('admin_users', None):
                site.admin_users.clear()
                for user in self.data['admin_users']:
                    site.admin_users.add(UserProfile.objects.get(id=user))
            
            site.save()
            return SiteSerializer(site).data
        except Exception as e:
            raise Exception(f'Error in updating site - {str(e)}')
    
    def delete_site(self, instance):
        try:
            #check_permissions
            instance.delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting site - {str(e)}')
    
    def update_area(self, area, id=None):
        try:
            if id:
                site = self.get_site_instance_by_id(id)
                area = dict(area)
                site.areas.add(area['id'])
                site.save()
            else:
                #TODO: flexibility to get called from create_site()
                pass
        except Exception as e:
            raise Exception(f'Error in updating area - {str(e)}')
                    
            
        
        
        
class ManageArea(FetchPermissions):
    def __init__(self, request=None):
        self.data = request.data
        self.request = request
        self.userprofile = self.__get_user()
        logging.info(f"Manage Area request: {self.data}")
        super().__init__(self.userprofile)
    
    def __get_user(self):
        return UserProfile.objects.get(user=self.request.user)
    
    def get_area_instance_by_id(self, area_id):
        try:
            return Area.objects.get(id=area_id)
        except Exception as e:
            raise Exception(f'Error in getting area by id - {str(e)}')
        
    def get_area(self, pk=None):
        try:
            if pk:
                area = self.get_area_instance_by_id(pk)
                permissions = self.get_permissions(area)
                if (
                    permissions['is_allowed'] or 
                    permissions['is_admin'] or 
                    permissions['is_super_admin']
                ):
                    serializer = SiteSerializer(area)
                else:
                    raise Exception('User not allowed to access this site')
            else:
                # GetAll Areas by User Permission Levels
                areas = self.permissions.fetch_all_permitted(Area)
                serializer = AreaSerializer(areas, many=True)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in getting area - {str(e)}')
        
    def get_areas_by_site_id(self, site_id):
        try:
            areas = Area.objects.filter(site_id=site_id)
            serializer = AreaSerializer(areas, many=True)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in getting areas by site_id - {str(e)}')
    
    def create_area(self):
        try:
            area = Area(
                name=self.data['name'],
                created_by=self.__get_user(),
                site_id = self.data['site_id'],
                description = self.data['description']
            )    
            area.save()      
                      
            if self.data.get('allowed_users', None):
                for user in self.data['allowed_users']:
                    area.allowed_users.add(user)
            if self.data.get('admin_users', None):
                for user in self.data['admin_users']:
                    area.admin_users.add(user)
            
            area.save()
                    
            area = AreaSerializer(area).data
            
            #Map this area to site requested for creation
            print(area)
            self._map_area_to_site(area)
            
            return area
        except Exception as e:
            raise Exception(f'Error in creating area - {str(e)}')
    
    def delete_area(self, instance):
        try:
            #check_permissions
            instance.delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting area - {str(e)}')
        
    def update_area(self, instance):
        try:
            instance.name = self.data['name']
            instance.site_id = self.data['site_id']
            instance.description = self.data['description']
            instance.save()
            
            if self.data.get('allowed_users', None):
                instance.allowed_users.clear()
                for user in self.data['allowed_users']:
                    instance.allowed_users.add(user)
                    
            if self.data.get('admin_users', None):
                instance.admin_users.clear()
                for user in self.data['admin_users']:
                    instance.admin_users.add(user)
                    
            if self.data.get('sites', None):
                instance.areas.clear()
                for area in self.data['areas']:
                    instance.areas.add(area)
                    
            instance.save()
            
            area = AreaSerializer(instance).data
            return area
            
        except Exception as e:
            raise Exception(f'Error in updating area - {str(e)}')
        
    
            
        
            
    
    def _map_area_to_site(self,area):
        try:
            ManageSite(self.request).update_area(area,id=self.data['site_id'])
        except Exception as e:
            raise Exception(f'Error in mapping area to site - {str(e)}')
    
    def update_lines(self, line, id=None):
        try:
            if id:
                area = self.get_area_instance_by_id(id)
                area.lines.add(line['id'])
                area.save()

            else:
                #TODO: flexibility to get called from create_area()
                pass
        except Exception as e:
            raise Exception(f'Error in updating lines - {str(e)}')        
        

class ManageLine(FetchPermissions):
    def __init__(self, request):
        self.data = request.data
        self.request = request
        self.userprofile = self.__get_user()
        logging.info(f"Manage Line request: {self.data}")
        super().__init__(self.userprofile)
        
    
    def __get_user(self):
        return UserProfile.objects.get(user=self.request.user)
    
    def get_line_instance_by_id(self, line_id):
        try:
            return Line.objects.get(id=line_id)
        except Exception as e:
            raise Exception(f'Error in getting line by id - {str(e)}')
    
    def get_lines_by_area_id(self,area_id):
        try :
            lines = Line.objects.filter(area_id = area_id)
            serializer = LineSerializer(lines, many=True)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in getting lines by area_id - {str(e)}')
        

        
    def get_line(self, pk=None):
        try:
            if pk:
                line = self.get_line_instance_by_id(pk)    
                permissions = self.get_permissions(line)
                if (
                    permissions['is_allowed'] or 
                    permissions['is_admin'] or 
                    permissions['is_super_admin']
                ):
                    serializer = AreaSerializer(line)
                else:
                    raise Exception('User not allowed to access this site')
            else:
                # GetAll Lines by User Permission Levels
                lines = self.permissions.fetch_all_permitted(Line)
                serializer = LineSerializer(lines, many=True)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in getting line - {str(e)}')
    
    def create_line(self):
        try:
            line = Line(
                name=self.data['name'],
                created_by=self.__get_user(),
                area_id = self.data['area_id'],
                site_id = self.data['site_id'],
                description = self.data['description']
            )
            
            line.save()
            print(line)
            if self.data.get('allowed_users', None):
                for user in self.data['allowed_users']:
                    line.allowed_users.add(user)
            if self.data.get('admin_users', None):
                for user in self.data['admin_users']:
                    line.admin_users.add(user)
            
            line.save()
            line = LineSerializer(line).data
            #Map this area to site requested for creation
            self._map_line_to_area(dict(line))
            
            return line
        except Exception as e:
            raise Exception(f'Error in creating line - {str(e)}')
        
    def update_line(self, instance):
        try:
            instance.name = self.data['name']
            instance.site_id = self.data['site_id']
            instance.area_id = self.data['area_id']
            instance.description = self.data['description']
            instance.save()
            
            if self.data.get('allowed_users', None):
                instance.allowed_users.clear()
                for user in self.data['allowed_users']:
                    instance.allowed_users.add(user)
                    
            if self.data.get('admin_users', None):
                instance.admin_users.clear()
                for user in self.data['admin_users']:
                    instance.admin_users.add(user)
                    
            if self.data.get('areas', None):
                instance.lines.clear()
                for line in self.data['lines']:
                    instance.lines.add(line)
                    
            instance.save()
            
            line = LineSerializer(instance).data
            return line
            
        except Exception as e:
            raise Exception(f'Error in updating line - {str(e)}')
    
    def delete_line(self, instance):
        try:
            #check_permissions
            instance.delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting line - {str(e)}')
    
    def _map_line_to_area(self,line):
        try:
            ManageArea(self.request).update_lines(line,id=self.data['area_id'])
        except Exception as e:
            raise Exception(f'Error in mapping line to area - {str(e)}')
        
    def update_processes(self, process, id=None):
        try:
            if id:
                line = self.get_line_instance_by_id(id)
                line.processes.add(process['id'])
                line.save()
            else:
                #TODO: flexibility to get called from create_line()
                pass
        except Exception as e:
            raise Exception(f'Error in updating processes - {str(e)}')
        
        
class ManageProcess(FetchPermissions):
    def __init__(self, request):
        self.request = request
        self.data = request.data
        self.userprofile = self.__get_user()
        logging.info(f"Manage Process request: {self.data}")
        super().__init__(self.userprofile)
    
    def __get_user(self):
        return UserProfile.objects.get(user=self.request.user)
    
    def get_process_instance_by_id(self, process_id):
        try:
            return Process.objects.get(id=process_id)
        except Exception as e:
            raise Exception(f'Error in getting process by id - {str(e)}')
        
    def get_processes_by_line_id(self,line_id):
        try : 
            processes = Process.objects.filter(line_id=line_id)
            serializer = ProcessSerializer(processes, many=True)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in getting processes by_line_id - {str(e)}')
    
    def get_process_choices(self):
        choices = []
        choices_dict = dict(Process.process_type.field.choices)
        
        for key, value in choices_dict.items():
            choices.append(dict(id=key, name=value))
        return choices
        
    def get_process(self, pk=None):
        try:
            if pk:
                process = self.get_process_instance_by_id(pk)
                permissions = self.get_permissions(process)
                if (
                    permissions['is_allowed'] or 
                    permissions['is_admin'] or 
                    permissions['is_super_admin']
                ):
                    serializer = SiteSerializer(process)
                else:
                    raise Exception('User not allowed to access this site')
            else:
                # GetAll Processes by User Permission Levels
                processes = self.permissions.fetch_all_permitted(Process)
                serializer = ProcessSerializer(processes, many=True)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in getting process - {str(e)}')
        
    def create_process(self):
        try:
            process = Process(
                name=self.data['name'],
                created_by=self.__get_user(),
                line_id = self.data['line_id'],
                area_id = self.data['area_id'],
                site_id = self.data['site_id'],
                process_type = self.data['process_type'],
                description = self.data['description']
            )
            
            process.save()
            
            if self.data.get('allowed_users', None):
                for user in self.data['allowed_users']:
                    process.allowed_users.add(user)
            if self.data.get('admin_users', None):
                for user in self.data['admin_users']:
                    process.admin_users.add(user)
            
            process.save()
            print(process)
            process = ProcessSerializer(process).data
            #Map this process to line requested for creation
            self._map_process_to_line(dict(process))      
            return process
        except Exception as e:
            logging.error(f'Error in creating process - {str(e)}')
            raise Exception(f'Error in creating process - {str(e)}')
    
    def update_processes(self, instance):
        try:
            instance.name = self.data['name']
            instance.line_id = self.data['line_id']
            instance.site_id = self.data['site_id']
            instance.area_id = self.data['area_id']
            instance.process_type = self.data['process_type']
            instance.description = self.data['description']
            instance.save()
            
            if self.data.get('allowed_users', None):
                instance.allowed_users.clear()
                for user in self.data['allowed_users']:
                    instance.allowed_users.add(user)
                    
            if self.data.get('admin_users', None):
                instance.admin_users.clear()
                for user in self.data['admin_users']:
                    instance.admin_users.add(user)
                    
            if self.data.get('lines', None):
                instance.processes.clear()
                for process in self.data['processes']:
                    instance.processes.add(process)
                    
            instance.save()
            
            process = ProcessSerializer(instance).data
            return process
            
        except Exception as e:
            raise Exception(f'Error in updating process - {str(e)}')
    
        
    def delete_process(self, instance):
        try:
            #check_permissions
            instance.delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting process - {str(e)}')
        
    
    def _map_process_to_line(self,process):
        try:
            ManageLine(self.request).update_processes(process,id=self.data['line_id'])
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
        
class ManageMachine(FetchPermissions):
    def __init__(self, request):
        self.request = request
        self.data = request.data
        self.userprofile = self.__get_user()
        logging.info(f"Manage Machine request: {self.data}")
        super().__init__(self.userprofile)
        
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
    
    def get_machine_choices(self):
        choices = []
        choices_dict = dict(Machine.machine_type.field.choices)
        
        for key, value in choices_dict.items():
            choices.append(dict(id=key, name=value))
        return choices
        
    def get_machine(self, pk=None):
        try:
            if pk:
                machine = self.get_machine_instance_by_id(pk)
                permissions = self.get_permissions(machine)
                if (
                    permissions['is_allowed'] or 
                    permissions['is_admin'] or 
                    permissions['is_super_admin']
                ):
                    serializer = SiteSerializer(machine)
                else:
                    raise Exception('User not allowed to access this site')
            else:
                # GetAll Machines by User Permission Levels
                machines = self.permissions.fetch_all_permitted(Machine)
                serializer = MachineSerializer(machines, many=True)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in getting machine - {str(e)}')
        
    def create_machine(self):
        try:
            machine = Machine(
                name=self.data['name'],
                machine_type=self.data['machine_type'],
                manufacturer=self.data['manufacturer'],
                model_number=self.data['model_number'],
                serial_number=self.data['serial_number'],
                description = self.data['description'],
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
        
    def update_machines(self, instance):
        try:
            instance.name = self.data['name']
            instance.machine_type = self.data['machine_type']
            instance.manufacturer = self.data['manufacturer']
            instance.model_number= self.data['model_number']
            instance.serial_number = self.data['serial_number']
            instance.is_active = self.data['is_active']
            instance.description = self.data['description']
            instance.save()

            if self.data.get('allowed_users', None):
                instance.allowed_users.clear()
                for user in self.data['allowed_users']:
                    instance.allowed_users.add(user)
                    
            if self.data.get('admin_users', None):
                instance.admin_users.clear()
                for user in self.data['admin_users']:
                    instance.admin_users.add(user)
                    
            if self.data.get('machines', None):
                instance.machines.clear()
                for machine in self.data['machines']:
                    instance.machines.add(machine)
                    
            instance.save()
            
            machine = MachineSerializer(instance).data
            return machine
            
        except Exception as e:
            raise Exception(f'Error in updating machine - {str(e)}')

class ManageTagTopics(FetchPermissions):
    def __init__(self, request):
        self.request = request
        self.data = request.data
        self.userprofile = self.__get_user()
        logging.info(f"Manage TagTopics request: {self.data}")
        super().__init__(self.userprofile)
    
    def __get_user(self):
        return UserProfile.objects.get(user=self.request.user)
    
    def get_tagtopics_instance_by_id(self, tag_id):
        try:
            return TagTopics.objects.get(id=tag_id)
        except Exception as e:
            raise Exception(f'Error in getting tag by id - {str(e)}')
        
    def create_tagtopics(self):
        try:
            tagtopics = TagTopics(
                name = self.data['name'], 
                machine_id = self.data['machine_id'],
                area_id = self.data['area_id'],
                site_id = self.data['site_id'],
                line_id = self.data['line_id'],
                value = self.data['value'],
                topic = self.data['topic'],
                description = self.data['description'],
                # process = self.data['process']              
            )           
            tagtopics.save()
            print(tagtopics)
            serializer = TagTopicsSerializer(tagtopics)
            return serializer.data
        except Exception as e:
            logging.error(f'Error in creating tags - {str(e)}')
            raise Exception(f'Error in creating tags - {str(e)}')
    
    def update_tagtopics(self, instance):
        try:
            instance.name = self.data['name']
            instance.line_id = self.data['line_id']
            instance.site_id = self.data['site_id']
            instance.area_id = self.data['area_id']
            instance.machine_id = self.data['machine_id']
            instance.value = self.data['value']
            instance.topic = self.data['topic']
            instance.description = self.data['description']
            instance.save()      
            tags = TagTopicsSerializer(instance).data
            return tags
            
        except Exception as e:
            raise Exception(f'Error in updating tags - {str(e)}')
    
        
    def delete_tags(self, instance):
        try:
            #check_permissions
            instance.delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting tags - {str(e)}')
                 

class ManageOrganization:
    def __init__(self, request):
        self.request = request
        self.data = request.data
        
        logging.info(f"Manage Organization request: {self.data}")
        
    def __get_user(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except Exception as e:
            raise Exception(f'Error in getting user - {str(e)}')
        
    def get_organization_instance_by_id(self, organization_id):
        try:
            return Organization.objects.get(id=organization_id)
        except Exception as e:
            raise Exception(f'Error in getting organization by id - {str(e)}')
        
   
    def update_organization(self):
        try:
            if id:
                organization = self.get_organization_instance_by_id(id)
                organization.org_name = self.data['org_name']
                organization.org_img = self.data['org_img']
                organization.address = self.data['address']
                organization.owners = self.data['owners']
                organization.save()
            else:
                pass
        except Exception as e:
            raise Exception(f'Error in updating organization - {str(e)}')
        
        
class ManageMyDashboard():
    
    def __init__(self, request):
        self.request = request
        self.data = request.data
        
        logging.info(f"Manage My Dashboard request: {self.data}")
    
    def __get_user(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except Exception as e:
            raise Exception(f'Error in getting user - {str(e)}')
        
    
    def get_my_dashboards(self):
        try:
            dashboards = MyDashboard.objects.filter(created_by=self.__get_user())
            serializer = MyDashboardSerializer(dashboards, many=True)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in getting my dashboards - {str(e)}')
        
    def get_my_default_dashboard(self):
        try:
            dashboard = MyDashboard.objects.get(created_by=self.__get_user(), is_default=True)
            serializer = MyDashboardSerializer(dashboard)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in getting my default dashboard - {str(e)}')
        
    
    def create_my_dashboard(self):
        try:
            dashboard = MyDashboard(
                name=self.data['name'],
                created_by=self.__get_user(),
                is_default=False,
                widgets=self.data['widgets']
            )
            dashboard.save()
            serializer = MyDashboardSerializer(dashboard)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in creating my dashboard - {str(e)}')
        
    def update_my_dashboard(self):
        try:
            dashboard = MyDashboard.objects.get(id=self.data['id'])
            dashboard.name = self.data['name']
            dashboard.widgets = self.data['widgets']
            dashboard.is_default = self.data['is_default']
            dashboard.save()
            serializer = MyDashboardSerializer(dashboard)
            return serializer.data
        except Exception as e:
            raise Exception(f'Error in updating my dashboard - {str(e)}')
        
    def delete_my_dashboard(self, instance):
        try:
            MyDashboard.objects.get(id=instance).delete()
            return True
        except Exception as e:
            raise Exception(f'Error in deleting my dashboard - {str(e)}')