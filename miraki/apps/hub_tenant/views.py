import logging
from typing import List
from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
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
        
class InviteUserApi(APIView):
    
    @extend_schema(
        methods=['POST'],
        parameters=[
            OpenApiParameter(
                name='email',
                type=str,
                location=OpenApiParameter.PATH,
                description='Your parameter description',
            ),
        ]
        )
    def post(self, request, *args, **kwargs):
        logging.info(f"Invite user request: {request.data}")
        try:
            invite_user_form = InviteUserForm(request.data)
            if invite_user_form.is_valid():
                ManageUser(request).invite_user()
            else:
                return Response({'message': 'Error inviting user', 'error': invite_user_form.errors}, status=400)
            return Response({'message': 'User invited successfully!'}, status=200)
        except Exception as e:
            return Response({'message': 'Error inviting user', 'error': str(e)}, status=400)

@permission_classes([])
class IsUserExists(APIView):
    
    @extend_schema(
    parameters=[
        OpenApiParameter(
            name='id',
            type=str,
            location=OpenApiParameter.QUERY,
            description='Your parameter description',
            enum=[],
        )
    ]
    )
    def get(self, request, *args, **kwargs):
        logging.info(f"Is user exists ? : {request.query_params}")
        try:
            if user_id := request.query_params.get('id', None):
                userprofile = ManageUser().get_user_profile(user_id)
                logging.info(f"User profile: {userprofile}")
                return Response(userprofile, status=200)
            else:
                return Response({'message': 'User ID is required'}, status=400)
        except Exception as e:
            return Response({'message': 'User Does Not Exist', 'error': str(e)}, status=400)
        
        
@permission_classes([])
class UserOnboardApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_onboard_form = UserOnboardForm(request.data)
            if not user_onboard_form.is_valid():
                return Response({'message': 'Error activating user account', 'error': user_onboard_form.errors}, status=400)
            ManageUser(request).onboard_user()
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
            logging.info("User profile request:")
            userprofile = UserProfile.objects.all()
            serializer = UserProfileSerializer(userprofile, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'message': 'Error fetching user profile', 'error': str(e)}, status=400)
    
    def update(self, request, *args, **kwargs):
        try:
            logging.info(f"Update user profile request: {request.data}")
            userprofile = ManageUser(request).update_userprofile()
            return Response(userprofile, status=200)
        except Exception as e:
            return Response({'message': 'Error updating user profile', 'error': str(e)}, status=400)
    

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    
    def list(self, request, *args, **kwargs):
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data, status=200)
    
    def update(self, request, *args, **kwargs):
        try:
            logging.info(f"Update organization request: {request.data}")
            organization = ManageOrganization(request).update_organization()
            return Response(organization, status=200)
        except Exception as e:
            return Response({'message': 'Error updating organization', 'error': str(e)}, status=400)
    
class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    
    def retrieve(self, request, *args, **kwargs):
        # The Primary Key of the object is passed to the retrieve method through self.kwargs
        object_id = self.kwargs['pk']
        site = ManageSite(request).get_site(object_id)
        return Response(site, status=200)
    
    def list(self, request, *args, **kwargs):
        sites = ManageSite(request).get_site()
        return Response(sites, status=200)
    

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
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            siteform = SiteForm(request.data)
            if not siteform.is_valid():
                return Response({'message': 'Error updating site', 'error': siteform.errors}, status=400)
            site = ManageSite(request).update_site(instance)
            return Response(site, status=200)
        except Exception as e:
            logging.error(f"Error updating site: {str(e)}")
            return Response({'message': 'Error updating site', 'error': str(e)}, status=400)
        
class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    
    def retrieve(self, request, *args, **kwargs):
        # The Primary Key of the object is passed to the retrieve method through self.kwargs
        object_id = self.kwargs['pk']
        data = ManageArea(request).get_area(object_id)
        return Response(data, status=200)
    
    def list(self, request, *args, **kwargs):
        areas = ManageArea(request).get_area()
        return Response(areas, status=200)
    
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
        
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            areaform = AreaForm(request.data)
            if not areaform.is_valid():
                return Response({'message': 'Error updating area', 'error': areaform.errors}, status=400)
            area = ManageArea(request).update_area(instance)
            return Response(area, status=200)
        except Exception as e:
            logging.error(f"Error updating area: {str(e)}")
            return Response({'message': 'Error updating area', 'error': str(e)}, status=400)
    
class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    
    def retrieve(self, request, *args, **kwargs):
        # The Primary Key of the object is passed to the retrieve method through self.kwargs
        object_id = self.kwargs['pk']
        data = ManageLine(request).get_line(object_id)
        return Response(data, status=200)
    
    def list(self, request, *args, **kwargs):
        lines = ManageLine(request).get_line()
        return Response(lines, status=200)
    
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
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            lineform = LineForm(request.data)
            if not lineform.is_valid():
                return Response({'message': 'Error updating line', 'error': lineform.errors}, status=400)
            line = ManageLine(request).update_line(instance)
            return Response(line, status=200)
        except Exception as e:
            logging.error(f"Error updating line: {str(e)}")
            return Response({'message': 'Error updating line', 'error': str(e)}, status=400)
        
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
    
    def retrieve(self, request, *args, **kwargs):
        # The Primary Key of the object is passed to the retrieve method through self.kwargs
        object_id = self.kwargs['pk']
        data = ManageProcess(request).get_process(object_id)
        return Response(data, status=200)
    
    def list(self, request, *args, **kwargs):
        processes = ManageProcess(request).get_process()
        return Response(processes, status=200)
    
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
        
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            processform = ProcessForm(request.data)
            if not processform.is_valid():
                return Response({'message': 'Error updating process', 'error': processform.errors}, status=400)
            process = ManageProcess(request).update_processes(instance)
            return Response(process, status=200)
        except Exception as e:
            logging.error(f"Error updating process: {str(e)}")
            return Response({'message': 'Error updating process', 'error': str(e)}, status=400)

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
    
    def retrieve(self, request, *args, **kwargs):
        # The Primary Key of the object is passed to the retrieve method through self.kwargs
        object_id = self.kwargs['pk']
        data = ManageMachine(request).get_machine(object_id)
        return Response(data, status=200)
    
    def list(self, request, *args, **kwargs):
        machines = ManageMachine(request).get_machine()
        return Response(machines, status=200)
    
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
    
    
class MyDashboardViewSet(viewsets.ModelViewSet):
    queryset = MyDashboard.objects.all()
    serializer_class = MyDashboardSerializer
    
    def list(self, request, *args, **kwargs):
        try:
            mydashboard = ManageMyDashboard(request).get_my_dashboards()
            return Response(mydashboard, status=200)
        except MyDashboard.DoesNotExist:
            return Response({'message': 'No Dashboard not found'}, status=200)
        except Exception as e:
            return Response({'message': 'Error fetching dashboard', 'error': str(e)}, status=400)
    
    def create(self, request, *args, **kwargs):
        try:
            mydashboard = ManageMyDashboard(request).create_my_dashboard()
            return Response(mydashboard, status=200)
        except Exception as e:
            return Response({'message': 'Error creating dashboard', 'error': str(e)}, status=400)
    
    def update(self, request, *args, **kwargs):
        try:
            mydashboard = ManageMyDashboard(request).update_my_dashboard()
            return Response(mydashboard, status=200)
        except Exception as e:
            return Response({'message': 'Error updating dashboard', 'error': str(e)}, status=400)
        
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            ManageMyDashboard(request).delete_my_dashboard(instance)
            return Response({'message': 'Dashboard deleted successfully!'}, status=200)
        except Exception as e:
            return Response({'message': 'Error deleting dashboard', 'error': str(e)}, status=400)
            