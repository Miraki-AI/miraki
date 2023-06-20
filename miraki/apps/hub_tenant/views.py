import logging
from typing import List
from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.authtoken.views import APIView
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .serializer import UserProfileSerializer
from .models import UserProfile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image

from miraki.apps.hub_tenant.mediatr import *
from miraki.apps.hub_tenant.forms import *
from miraki.apps.hub_tenant.models import *
from miraki.apps.hub_tenant.serializer import *
# Create your views here.
class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        userprofile = UserProfileSerializer(UserProfile.objects.get(user=user)).data
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.pk,
            'email': user.email,
            'userprofile':userprofile
        })
        

class UserOnboardApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_onboard_form = UserOnboardForm(request.data)
            if not user_onboard_form.is_valid():
                return Response({'message': 'Error activating user account', 'error': user_onboard_form.errors}, status=400)
            UserOnBoard(request).onboard_user()
            return Response({'message': 'User account activated successfully!'}, status=200)
        except Exception as e:
            return Response({'message': 'Error activating user account', 'error': str(e)}, status=400)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.all()
    
    def list(self, request, *args, **kwargs):
        try:
            logging.info(f"User profile request: {request.tenant}")
            userprofile = UserProfile.objects.all()
            serializer = UserProfileSerializer(userprofile, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'message': 'Error fetching user profile', 'error': str(e)}, status=400)
    

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    
    def list(self, request, *args, **kwargs):
        sites = Site.objects.all()
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data, status=200)
    

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='address',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Your parameter description',
                enum=[],
            ),
            OpenApiParameter(
                name='city',
                type=str
            ),
            OpenApiParameter(
                name='country',
                type=str
            ),
            OpenApiParameter(
                name='zipcode',
                type=str
            ),
            OpenApiParameter(
                name='allowed_users',
                type={'type': 'array', 'items': {'type': 'string'}},
            ),
            OpenApiParameter(
                name='admin_users',
                type={'type': 'array', 'items': {'type': 'string'}},
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        try:
            siteform = SiteForm(request.data)
            if not siteform.is_valid():
                return Response({'message': 'Error creating site', 'error': siteform.errors}, status=400)
            site = ManageSite(request).create_site()
            return Response(site, status=200)
        except Exception as e:
            logging.error(f"Error creating site: {str(e)}")
            return Response({'message': 'Error creating site', 'error': str(e)}, status=400)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            ManageSite(request).delete_site(instance)
            return Response({'message': 'Site deleted successfully!'}, status=200)
        except Exception as e:
            return Response({'message': 'Error deleting site', 'error': str(e)}, status=400)
        
        
class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    
    def list(self, request, *args, **kwargs):
        areas = Area.objects.all()
        serializer = AreaSerializer(areas, many=True)
        return Response(serializer.data, status=200)
    
    def create(self, request, *args, **kwargs):
        try:
            areaform = AreaForm(request.data)
            if not areaform.is_valid():
                return Response({'message': 'Error creating area', 'error': areaform.errors}, status=400)
            area = ManageArea(request).create_area()
            return Response(area, status=200)
        except Exception as e:
            logging.error(f"Error creating area: {str(e)}")
            return Response({'message': 'Error creating area', 'error': str(e)}, status=400)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            ManageArea(request).delete_area(instance)
            return Response({'message': 'Area deleted successfully!'}, status=200)
        except Exception as e:
            return Response({'message': 'Error deleting area', 'error': str(e)}, status=400)
    
class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    
    def list(self, request, *args, **kwargs):
        lines = Line.objects.all()
        serializer = LineSerializer(lines, many=True)
        return Response(serializer.data, status=200)
    
    def create(self, request, *args, **kwargs):
        try:
            lineform = LineForm(request.data)
            if not lineform.is_valid():
                return Response({'message': 'Error creating line', 'error': lineform.errors}, status=400)
            line = ManageLine(request).create_line()
            return Response(line, status=200)
        except Exception as e:
            logging.error(f"Error creating line: {str(e)}")
            return Response({'message': 'Error creating line', 'error': str(e)}, status=400)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            ManageLine(request).delete_line(instance)
            return Response({'message': 'Line deleted successfully!'}, status=200)
        except Exception as e:
            return Response({'message': 'Error deleting line', 'error': str(e)}, status=400)


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    
    def list(self, request, *args, **kwargs):
        processes = Process.objects.all()
        serializer = ProcessSerializer(processes, many=True)
        return Response(serializer.data, status=200)
    
    def create(self, request, *args, **kwargs):
        try:
            processform = ProcessForm(request.data)
            if not processform.is_valid():
                return Response({'message': 'Error creating process', 'error': processform.errors}, status=400)
            process = ManageProcess(request).create_process()
            return Response(process, status=200)
        except Exception as e:
            logging.error(f"Error creating process: {str(e)}")
            return Response({'message': 'Error creating process', 'error': str(e)}, status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            ManageProcess(request).delete_process(instance)
            return Response({'message': 'Process deleted successfully!'}, status=200)
        except Exception as e:
            return Response({'message': 'Error deleting process', 'error': str(e)}, status=400)


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    
    def list(self, request, *args, **kwargs):
        machines = Machine.objects.all()
        serializer = MachineSerializer(machines, many=True)
        return Response(serializer.data, status=200)
    
    def create(self, request, *args, **kwargs):
        try:
            machineform = MachineForm(request.data)
            if not machineform.is_valid():
                return Response({'message': 'Error creating machine', 'error': machineform.errors}, status=400)
            machine = ManageMachine(request).create_machine()
            return Response(machine, status=200)
        except Exception as e:
            logging.error(f"Error creating machine: {str(e)}")
            return Response({'message': 'Error creating machine', 'error': str(e)}, status=400)

class TagTopicsViewSet(viewsets.ModelViewSet):
    queryset = TagTopics.objects.all()
    serializer_class = TagTopicsSerializer
    
    def list(self, request, *args, **kwargs):
        tag_topics = TagTopics.objects.all()
        serializer = TagTopicsSerializer(tag_topics, many=True)
        return Response(serializer.data, status=200)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        logging.info(f"Tag Topics data: {data}")
        tag_topics = TagTopics.objects.create(name=data['name'], machine_id=data['machine_id'])
        serializer = TagTopicsSerializer(tag_topics)
        return Response(serializer.data, status=200)