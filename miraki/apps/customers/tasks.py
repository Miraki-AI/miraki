from .mediatr import Tenant
from celery import shared_task
import logging

@shared_task
def create_tenant(data):
    try:
        Tenant(data).create_tenant()
    except Exception as e:
        logging.error(f"Error creating tenant: {str(e)}")
    
    