from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


from faker import Faker
import logging
import logging.config

from posts.models import Post
from comments.models import Comment


class Command(BaseCommand):
    help = 'Seed the Comment database'

    def add_arguments(self, parser):
        parser.add_argument('--comment',
                            default=10,
                            type=int,
                            help='The number of user you want to create.')

    def handle(self, *args, **kwargs):
        logging.config.fileConfig(fname='logs/log.conf')
        logger = logging.getLogger('comments')
        logger.info('Comments Data Creating..')
        try:
            post_ids = Post.objects.all().values_list('id', flat=True)
            fake = Faker()
            for post_id in post_ids:
                for x in range(kwargs['comment']):
                    user = fake.random_element(User.objects.all())
                    object_id = post_id
                    content = fake.text(max_nb_chars=500)
                    content_type = ContentType.objects.get(app_label__iexact='posts', model__iexact='post')
                    Comment.objects.create(user=user, object_id=object_id, content=content, content_type=content_type)
            logger.info(f'Post Data Created')
        except Exception as e:
            logger.info(f'Post Creation Error: {e}')

