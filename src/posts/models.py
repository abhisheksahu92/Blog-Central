from django.db import models
from django.urls import reverse

def upload_location(instance,filename):
    return f'{instance.id}/{filename}'

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to = upload_location,
                    null=True,blank=True,height_field='height_field',width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateField(auto_now=True,auto_now_add=False)
    created = models.DateField(auto_now=False,auto_now_add=True)

    
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:postdetails',kwargs={'id':self.id})

    def get_absolute_url_update(self):
        return reverse('posts:postupdate',kwargs={'id':self.id})

    def get_absolute_url_delete(self):
        return reverse('posts:postdelete',kwargs={'id':self.id})

    class Meta:
        ordering = ['-updated','-created']
    