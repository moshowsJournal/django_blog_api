from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete,pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import random
# Create your models here.

def upload_location(instance,filename):
    file_path = '/blog/{author_id}-{title}-{file_name}'.format(
        author_id=str(instance.author.id),title=str(instance.title),file_name=filename
    )
    return file_path

class BlogPost(models.Model):
    title = models.CharField(max_length=100,null=False,blank=True)
    body = models.TextField(max_length=300,null=False,blank=False)
    image = models.ImageField(upload_to=upload_location,null=True,blank=True)
    is_published = models.BooleanField(default=False)
    date_published = models.DateTimeField(auto_now_add=True,verbose_name='date published')
    date_updated = models.DateTimeField(auto_now=True,verbose_name='date updated')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100,blank=True,unique=True)

    def __str__(self):
        return '{title}-{id}'.format(title=self.title,id=self.id)

@receiver(post_delete,sender=BlogPost)
def delete_image_file(sender,instance,*args,**kwargs):
    return instance.image.delete(True)

@receiver(pre_save,sender=BlogPost)
def before_save(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug =  slugify('{email}-{title}-{random_num}'.format(
            email=instance.author.email,title=instance.title,random_num=random.randint(1000,100000)
        ))
