import os  
import uuid 
from io import BytesIO 
from PIL import Image 
from datetime import datetime, timedelta 
from django.db import models
from django.utils.text import slugify 
from django.core.files.uploadedfile import InMemoryUploadedFile 
from django.core.exceptions import ValidationError 
from django.contrib.auth import get_user_model 

from core.timestamp import TimeStampModel 

User = get_user_model()



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
    is_index        = models.BooleanField(default=True) 
    uid             = models.CharField(max_length=32, default=generate_unique_uid, unique=True) 


    class Meta:
        ordering = ['-created'] 


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
    meta_keywords  = models.TextField(null=True, blank=True)
    meta_robots    = models.BooleanField(default=False) 
    is_index       = models.BooleanField(default=True) 
    is_active      = models.BooleanField(default=True)
    uid            = models.CharField(max_length=32, default=generate_unique_uid, unique=True)


    class Meta:
        ordering = ['-created']  


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
    published_at        = models.BooleanField(default=False)    
    scheduled_at        = models.DateTimeField(null=True, blank=True)
    approve             = models.BooleanField(default=True)
    tracking_id         = models.UUIDField(default=uuid.uuid4, unique=True, editable=False) 
    is_active           = models.BooleanField(default=True)
    views_count         = models.PositiveIntegerField(default=0)
    read_time           = models.PositiveIntegerField(null=True, blank=True)
    uid                 = models.CharField(max_length=32, default=generate_unique_uid, unique=True)


    class Meta:
        ordering = ['-created'] 


    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title) 
        super().save(*args, **kwargs)


    def __str__(self)-> str:
        return f'{self.title}'
    

    



def article_image_path(instance, filename):
    """Generate a unique file path for article images."""
    base, ext = os.path.splitext(filename)
    ext = ext.lower() if ext else ''
    filename = f'{uuid.uuid4().hex}{ext}'
    article_id = str(instance.article.id) if instance.article and instance.article.id else 'unknown'
    now = datetime.now()
    date_path = now.strftime('%Y/%m/%d')
    return os.path.join('article', 'images', date_path, article_id, filename)


class ArticleImageModel(TimeStampModel):
    """
    Model for Article images
    """
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE, null=True, blank=True, related_name='images')
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='images')
    image = models.ImageField(upload_to=article_image_path, null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return f'{self.article.title if self.article and self.article.title else "No Article"}'

    def clean(self):
        """Validate ArticleImageModel fields."""
        if self.article and (not self.article.title or len(self.article.title) < 5):
            raise ValidationError("Article title must be at least 5 characters long.")
        if self.image:
            ext = os.path.splitext(self.image.name)[1].lower()
            allowed_extension = ['.jpg', '.jpeg', '.png', '.gif']
            if ext not in allowed_extension:
                raise ValidationError(f"Unsupported file extension: {ext}")

    def make_thumbnail(self):
        """
        Create a thumbnail and compress the image to be below 150KB while maintaining quality.
        Maintains original format if not JPEG.
        """
        try:
            with Image.open(self.image) as img:
                # Convert to RGB if not already
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Resize to max 800x800 using LANCZOS for good quality
                img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                # Determine format
                orig_format = img.format if img.format in ['JPEG', 'PNG', 'GIF'] else 'JPEG'
                image_io = BytesIO()
                quality = 95
                save_kwargs = {'format': orig_format, 'optimize': True}
                if orig_format == 'JPEG':
                    save_kwargs['quality'] = quality
                img.save(image_io, **save_kwargs)
                # Compress if larger than 150KB (only for JPEG)
                if orig_format == 'JPEG' and image_io.tell() / 1024 > 150:
                    for quality in range(90, 69, -5):
                        image_io.seek(0)
                        img.save(image_io, format='JPEG', quality=quality, optimize=True)
                        if image_io.tell() / 1024 <= 150:
                            break
                    else:
                        raise ValidationError("Image is too large to compress below 150KB.")
                image_io.seek(0)
                processed_image = InMemoryUploadedFile(
                    image_io,
                    field_name=None,
                    name=os.path.basename(self.image.name),
                    content_type=f'image/{orig_format.lower()}',
                    size=image_io.tell(),
                    charset=None
                )
                return processed_image
        except Exception as e:
            raise ValidationError(f"Error creating thumbnail: {str(e)}")

    def save(self, *args, **kwargs):
        """
        Save method to process the image before saving.
        """
        if self.image:
            self.image = self.make_thumbnail()
        super().save(*args, **kwargs)