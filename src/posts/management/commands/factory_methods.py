import factory
from django.contrib.auth.models import User
from faker import Faker
import dumper

from posts.models import Post

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = User.objects.get(username='asahu')
    title = factory.Faker('name')
    content = factory.Faker('text')
    publish = factory.Faker('date')