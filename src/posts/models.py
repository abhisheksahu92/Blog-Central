from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    updated = models.DateField(auto_now=True,auto_now_add=False)
    created = models.DateField(auto_now=False,auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:postdetails',kwargs={'id':self.id})
    