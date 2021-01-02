# import factory
# from django.contrib.auth.models import User
# from faker import Faker
#
# from posts.models import Post
#
# User.objects.all()
#
# class PostFactory(factory.django.DjangoModelFactory):
#
#     class Meta:
#         model = Post
#
#
#     user = Faker().random_element(User.objects.all())
#     title = factory.Faker('name')
#     content = fake
#     publish = factory.Faker('date')