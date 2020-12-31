import sys,os
from django.core.management.base import BaseCommand
from django.db import transaction
import logging
import logging.config

from posts.models import Post

from .factory_methods import PostFactory

class Command(BaseCommand):
    help = 'Seed the Post database'

    def add_arguments(self, parser):
        parser.add_argument('--posts',
                            default=50,
                            type=int,
                            help='The number of posts you want to create.')

    @transaction.atomic
    def handle(self,*args,**kwargs):
        logging.config.fileConfig(fname='logs/log.conf')
        logger = logging.getLogger('posts')

        logger.info('Post Data Creating..')
        try:
            for x in range(kwargs['posts']):
                PostFactory.create()
            logger.info(f'{x+1} Post Data Created')
        except Exception as e:
            logger.info(f'Post Creation Error: {e}')


