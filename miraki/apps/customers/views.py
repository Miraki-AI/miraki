import logging
from django.shortcuts import render
from .models import Organization
from .forms import NewTenantForm
from .mediatr import Tenant
from .tasks import create_tenant

from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
# Create your views here.

class TenantApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            new_tenant = NewTenantForm(request.data)
            logging.info(f"New tenant: {new_tenant.data}")
            if not new_tenant.is_valid():
                return Response({'message':'Error creating organization', 'error': new_tenant.errors}, status=400)
            create_tenant.delay(new_tenant.data)
            return Response({'message':'Organization created successfully!'}, status=200)
        except Exception as e:
            return Response({'message':'Error creating organization', 'error': str(e)}, status=400)
        

