from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import logging
import logging.config
import factory

from posts.models import Post

class Command(BaseCommand):
    help = 'Seed the Post database'

    def add_arguments(self, parser):
        parser.add_argument('--posts',
                            default=50,
                            type=int,
                            help='The number of posts you want to create.')

    def handle(self,*args,**kwargs):
        user = User.objects.all()
        fake = Faker()
        posts = []
        logging.config.fileConfig(fname='logs/log.conf')
        logger = logging.getLogger('posts')

        logger.info('Post Data Creating..')
        try:
            for x in range(kwargs['posts']):
                user = fake.random_element(User.objects.all())
                title = fake.name()
                content = fake.text(max_nb_chars=500)
                publish = fake.date()
                # posts.append(Post(user=user,title=title,content=content,publish=publish))
            # Post.objects.bulk_create(posts)
                Post.objects.create(user=user,title=title,content=content,publish=publish)
            logger.info(f'{x+1} Post Data Created')
        except Exception as e:
            logger.info(f'Post Creation Error: {e}')


