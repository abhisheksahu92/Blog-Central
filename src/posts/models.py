from django.db import models
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown
from django.utils import timezone
from django.utils.timezone import localtime,get_default_timezone
from django.conf import settings

from comments.models import Comment
from .utils import get_read_time

class PostManager(models.Manager):
    def active(self,*args, **kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte = timezone.now())


def upload_location(instance,filename):
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    return "%s/%s" %(new_id, filename)

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique = True)
    image = models.ImageField(upload_to = upload_location,
                    null=True,blank=True,height_field='height_field',width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    draft = models.BooleanField(default = False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    read_time = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateField(auto_now=True,auto_now_add=False)
    created = models.DateField(auto_now=False,auto_now_add=True)


    objects = PostManager()
    
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_api_url(self):
        return reverse("posts-api:postapidetails", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return reverse('posts:postdetails',kwargs={"slug": self.slug})

    def get_absolute_url_update(self):
        return reverse('posts:postupdate',kwargs={"slug": self.slug})

    def get_absolute_url_delete(self):
        return reverse('posts:postdelete',kwargs={"slug": self.slug})

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)
    
    class Meta:
        ordering = ['-updated','-created']

    @property
    def comment(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
        
    
    
def pre_save_post_reciever(sender,instance,*args, **kwargs):
    slug = slugify(instance.title)
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exist = qs.exists()
    if exist:
        slug = '%s-%s' %(slug,qs.first().id)
    instance.slug = slug

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_reciever,sender=Post)