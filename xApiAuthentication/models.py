import os 
import sys 
import uuid 
from PIL import Image 
from io import BytesIO 

from django.db import models 
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.files.uploadedfile import InMemoryUploadedFile 

from xApiAuthentication.managers import CustomUserManager

def uload_to(instance, filename):
    ext         = filename.split('.')[-1]
    filename    = f'{uuid.uuid4()}.{ext}'

    return os.path.join(f'user_{instance.pk}', 'profile', filename)

class GenderChoices(models.TextChoices):
    MALE        = 'M', 'Male'
    FEMALE      = 'F', 'Female'
    OTHER       = 'C', 'Custom'

class CustomUser(AbstractUser, PermissionsMixin):
    email           = models.EmailField(unique=True)
    phn_num         = models.CharField(max_length=15, null=True, blank=True)
    gender          = models.CharField(max_length=10, choices=GenderChoices.choices, null=True, blank=True)
    dt_of_birth     = models.DateField(null=True, blank=True)
    pro_photo       = models.ImageField(upload_to=uload_to, null=True, blank=True)

    objects         = CustomUserManager()
    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username',]

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'


    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_user = CustomUser.objects.get(pk=self.pk)
                if old_user.pro_photo != self.pro_photo and old_user.pro_photo:
                    if os.path.isfile(old_user.pro_photo.path):
                        os.remove(old_user.pro_photo.path)
            except CustomUser.DoesNotExist:
                pass

        if self.pro_photo:
            thumb = self.make_thumbnail()
            if thumb:
                self.pro_photo = InMemoryUploadedFile(
                    file=thumb,
                    field_name='ImageField',
                    name='thumb.jpg',
                    content_type='image/jpeg',
                    size=thumb.getbuffer().nbytes,
                    charset=None
                )

        super().save(*args, **kwargs)  # ❗ This was missing!

    def make_thumbnail(self):
        try:
            self.pro_photo.seek(0)
            image = Image.open(self.pro_photo)
            image.thumbnail((300, 300))

            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            image_io = BytesIO()
            quality = 85

            while quality >= 30:
                image_io.seek(0)
                image_io.truncate()
                image.save(image_io, format='JPEG', quality=quality)
                size_kb = image_io.tell() / 1024
                if size_kb < 100:
                    break
                quality -= 5

            image_io.seek(0)
            return image_io

        except Exception as e:
            print(f"Thumbnail Error: {e}")
            return None
