
import os  
import sys 
import uuid 
from io import BytesIO 
from PIL import Image 
from django.db import models
from django.utils.text import slugify 
from django.core.files.uploadedfile import InMemoryUploadedFile 
from django.core.exceptions import ValidationError 
from django.contrib.auth import get_user_model 


User = get_user_model()



class TimeStampModel(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    modified   = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 


def generate_unique_uid():
    """ 
    Generate unique uid 
    """
    return uuid.uuid4().hex[:32].lower()
    


class ArticleCategoryModel(TimeStampModel):
    """ Model for Article category """
    cate_name       = models.CharField(max_length=512, unique=True)
    author          = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    is_active       = models.BooleanField(default=True)
    uid             = models.CharField(max_length=32, default=generate_unique_uid, unique=True) 


    def __str__(self):
        return f'{self.cate_name}-written-by-{self.author.email if self.author else "unknown"}'
    

class ArticleMetaTag(TimeStampModel):
    """ 
    Model for Article Meta Tag 
    """
    author         = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    tag            = models.CharField(max_length=255, null=True, blank=True)
    meta_title     = models.CharField(max_length=512, null=True, blank=True)
    meta_desc      = models.TextField(null=True, blank=True)
    meta_robots    = models.BooleanField(default=False) 
    is_active      = models.BooleanField(default=True)
    uid            = models.CharField(max_length=32, default=generate_unique_uid, unique=True)


    def __str__(self)-> str:
        return f'{self.tag}-{self.meta_title}' 




class ArticleModel(TimeStampModel):
    """ 
    Model for Article 
    """

    author              = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True )
    cate_id             = models.ForeignKey(ArticleCategoryModel, on_delete=models.CASCADE, null=True, blank=True)
    meta_tag            = models.ManyToManyField(ArticleMetaTag, blank=True)
    title               = models.CharField(max_length=255, null=True, blank=True)
    slug                = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    desc                = models.TextField()
    summary             = models.TextField(null=True, blank=True, help_text="Short summary for preview")
    featured_image      = models.ImageField(upload_to='article/covers/', null=True, blank=True)
    published_at        = models.BooleanField(default=False)    
    approve             = models.BooleanField(default=True)
    is_active           = models.BooleanField(default=True)
    views_count         = models.PositiveIntegerField(default=0)
    read_time           = models.PositiveIntegerField(null=True, blank=True)
    uid                 = models.CharField(max_length=32, default=generate_unique_uid, unique=True)


    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title) 
        super().save(*args, **kwargs)

    def __str__(self)-> str:
        return f'{self.title}'


def article_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex}.{ext}'
    article_slug = slugify(instance.article.slug if instance.article and instance.article.slug else 'unknown')
    return os.path.join('article', article_slug, 'images', filename)



class ArticleImageModel(TimeStampModel):
    """ 
    Model for Article images 
    """
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE, null=True, blank=True, related_name='images')
    author              = models.ForeignKey(User, on_delete=models.PROTECT,  null=True, blank=True,  related_name='images') 
    image               = models.ImageField(upload_to=article_image_path, null=True, blank=True)
    uid                 = models.UUIDField(default=uuid.uuid4, unique=True)

    
    def __str__(self)-> str:
        return f'{self.article.title}'
        


