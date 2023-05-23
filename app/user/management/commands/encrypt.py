from typing import Any
from django.core.management import BaseCommand
from core.encryption import decrypt, encrypt
from user.models import User
from datetime import datetime, timedelta
from random import randint

class Command(BaseCommand):
    
    def execute(self, *args, **options):
        
        for user in User.objects.all():
            User.objects.filter(email=None).delete()
            
            
        
