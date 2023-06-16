import logging
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template.loader import get_template
from miraki.users.api.serializers import UserSerializer
from .models import Organization, Domain
from miraki.apps.hub_tenant.models import UserProfile
from .serializers import *

from godaddypy import Client, Account
from celery import shared_task
import time
# `User = get_user_model()` is importing the user model defined in the Django project and assigning it
# to the variable `User`. This allows the code to create a new user object using the `User` model
# without having to hardcode the user model's name.
User = get_user_model()


class Tenant:
    def __init__(self, data):
        self.data = data
    
    def create_tenant(self):
        try:
            new_tenant = Organization.objects.create(
                schema_name=self.data['name'],
                name=self.data['name'], 
                paid_until='2025-10-10', 
                on_trial=False
            )
            new_domain = Domain.objects.create(
                domain=f"{self.data['name']}.miraki.ai",
                tenant=new_tenant,
                is_primary=True
            )
            logging.info(f"Domain created: {new_domain}")

            new_cname = self.create_cname_record()
            logging.info(f"CNAME record created: {new_cname}")
            
            time.sleep(600)
            self.send_email()    
            
            return True
        except Exception as e:
            logging.error(f"Error creating tenant: {str(e)}")
            return False
    
    def create_tenant_user(self):
        try:
            if user := User.objects.get_or_create(email=self.data['email']):
                UserProfile.objects.create(
                    name=f"{self.data['first_name']} {self.data['last_name']}",
                    email=self.data['email'],
                    user=User.objects.get(email=self.data['email']),
                    is_active=True,
                    is_admin=False,
                )

        except Exception as e:
            error = {
                'message': 'Error creating user',
                'status': 'False',
                'error': str(e)
            }
            logging.error(error)
            raise Exception(error)
    

    def create_cname_record(self):
        try:
            account = Account(api_key=settings.GODADDY_API_KEY, api_secret=settings.GODADDY_API_SECRET)
            client = Client(account)

            if result := client.add_record(
                settings.GODADDY_DOMAIN,
                {
                    'name': self.data['name'],
                    'ttl': 600,
                    'type': 'CNAME',
                    'data': settings.ELB_URL,
                },
            ):
                return {
                        'message': 'CNAME record created successfully!',
                        'status': 'True',
                        }
            else:
                return {
                    'message': 'Error creating CNAME record',
                    'status': 'False',
                    }
        except Exception as e:
            response = {
                    'message': 'Error creating CNAME record',
                    'status': 'False',
                    'error': str(e)
            }
            logging.info(response)
            return response
        
    def send_email(self):
        try:
            template = get_template('email/user_onboard.html')
            activation_url = f"http://{self.data['name']}.miraki.ai/core/api/tenant/activate?org_name={self.data['name']}&email={self.data['email']}"
            self.data['activation_url'] = activation_url
            subject = 'Welcome to Our Platform - User Onboarding'
            html_message = template.render({'data': self.data})
            send_mail(
                subject, 
                '', 
                from_email='vijenderpanda@miraki.ai', 
                recipient_list=['vijenderpanda@miraki.ai'], 
                html_message=html_message
            )
            return True
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            raise Exception(f"Error sending email: {str(e)}")
