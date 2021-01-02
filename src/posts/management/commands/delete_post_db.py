import sys,os
from django.core.management.base import BaseCommand
from django.db import transaction

from posts.models import Post

class Command(BaseCommand):
    help = 'Delete the Post database'

    @transaction.atomic
    def handle(self,*args,**kwargs):
        Post.objects.all().delete()