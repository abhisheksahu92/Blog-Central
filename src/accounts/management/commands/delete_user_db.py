import sys,os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q


class Command(BaseCommand):
    help = 'Delete the User database'

    @transaction.atomic
    def handle(self,*args,**kwargs):
        User.objects.filter(~Q(username = 'asahu')).delete()