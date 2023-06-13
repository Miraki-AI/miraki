import json
import os
from lexus.apps.hub.models import UserProfile, Organization, Facility, Module
from django.core.management import BaseCommand, call_command
from django.contrib.auth import get_user_model
import logging
User = get_user_model()

def get_or_create_user(email):
    try:
        return User.objects.get(username=email.split('@')[0])
    except User.DoesNotExist:

        user = User(
            is_staff = True,
            is_active = True,
            is_superuser = True,
            username = email.split('@')[0],
            email = email,
        )
        user.set_password("dev@123456")
        user.save()
        return user
        

def get_or_create_userprofile(email):
    try:
        userprofile = UserProfile.objects.get(email=email)
        logging.info(f"User profile {userprofile} already exists")
        return userprofile
    except UserProfile.DoesNotExist:
        user = get_or_create_user(email)
        userprofile = UserProfile.objects.create(
            email = email,
            user = user,
            name = user.username
        )
        return userprofile
    except:
        logging.error("Error creating user profile")
        raise Exception("Error creating user profile")
            

def should_load_data(record):
    """Return True if data should be loaded."""
    
    if record["model"] == "hub.userprofile":
        return not UserProfile.objects.filter(email=record["fields"]["email"]).exists()
    elif record["model"] == "hub.organization":
        return not Organization.objects.filter(id=record["pk"]).exists()
    elif record["model"] == "hub.facility":
        return not Facility.objects.filter(id=record["pk"]).exists()
    elif record["model"] == "hub.module":
        return not Module.objects.filter(id=record["pk"]).exists()

def loadFixtures(fixtures_path, fixture_name, user_create=False):
    with open(f'{fixtures_path}/{fixture_name}.json') as f:
        data = json.load(f)
        data_filtered = list(filter(should_load_data, data))
        if data_filtered:
            with open(f'{fixtures_path}/{fixture_name}_filtered.json', 'w') as f:
                json.dump(data_filtered, f)
        
            if user_create:      
                for user in data_filtered:
                    get_or_create_user(user["fields"]["email"])
                    
                    
            call_command("loaddata", f"{fixture_name}_filtered")
            os.remove(f'{fixtures_path}/{fixture_name}_filtered.json')
        
    