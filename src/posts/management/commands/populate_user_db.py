import sys,os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from faker import Faker
import logging
import logging.config

class Command(BaseCommand):
    help = 'Seed the User database'

    def add_arguments(self, parser):
        parser.add_argument('--user',
                            default=50,
                            type=int,
                            help='The number of user you want to create.')


    def handle(self,*args,**kwargs):

        logging.config.fileConfig(fname='logs/log.conf')
        logger = logging.getLogger('accounts')
        logger.info('User Data Creating..')

        try:
            faker = Faker()
            for x in range(kwargs['user']):
                profile = dict(faker.simple_profile())
                username = profile.get('username')
                first_name, last_name = profile.get('name').split(' ', 1)
                email = profile.get('mail')
                password = profile.get('name').replace(' ', '').title() + '@' + '123'
                User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                         password=password)
            logger.info(f'{x + 1} User Data Created')
        except Exception as e:
            logger.info(f'User Creation Error: {e}')

