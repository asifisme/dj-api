import os
import uuid
import sys
from datetime import datetime 
from io import BytesIO
from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from PIL import UnidentifiedImageError 
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError

from core.timestamp import TimeStampModel 



User = get_user_model()



def product_categor_unique_key() -> str:
    """
    Generate a unique key for the product category.
    """
    return uuid.uuid4().hex[:32].lower()


class ProductCategoryModel(TimeStampModel):
    """
    Model for product categories.
    """
    cate_name  = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug       = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    cate_desc  = models.TextField(null=True, blank=True)
    author     = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    uid        = models.CharField(max_length=255, default=product_categor_unique_key, unique=True)

    class Meta:
        ordering = ['-created']
        

    def __str__(self) -> str:
        return self.cate_name or "Unnamed Category"
    

    def save(self, *args, **kwargs):
        if self.cate_name and not self.slug:
            base_slug = slugify(self.cate_name)
            slug = base_slug
            counter = 1
            while ProductCategoryModel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)




class ProductCategoryImageModel(TimeStampModel):
    """ 
    Model for product categories 
    """
    pass 




def product_meta_tag_unique_key() -> str:
    """
    Generate a unique key for the product meta tag.
    """
    return uuid.uuid4().hex[:32].lower() 


class ProductMetaTagModel(TimeStampModel):
    """
    Model for product meta tags.
    """
    tag             = models.CharField(max_length=100, unique=True, null=True, blank=True)
    meta_title      = models.CharField(max_length=255, null=True, blank=True)
    meta_desc       = models.TextField(null=True, blank=True)
    meta_keywds     = models.TextField(null=True, blank=True)
    meta_robot      = models.BooleanField(default=False)
    is_indexed      = models.BooleanField(default=True)  
    author          = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    uid             = models.CharField(max_length=255, default=product_meta_tag_unique_key, unique=True)


    class Meta:
        ordering = ['-created']
       

    def __str__(self) -> str:
        return f"{self.meta_keywds or 'No Keywords'} - {self.meta_title or 'No Title'}"




def product_unique_number() -> str:
    """
    Generate a unique number for the product.
    """
    return str(uuid.uuid4().int % 10000000000000000000)


def product_unique_key() -> str:
    """
    Generate a unique key for the product.
    """
    return uuid.uuid4().hex[:32].lower() 


class ProductModel(TimeStampModel):
    """
    Model for products.
    """
    category             = models.ForeignKey(ProductCategoryModel, on_delete=models.PROTECT, null=True, blank=True)  
    author               = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    meta_tag             = models.ManyToManyField(ProductMetaTagModel, blank=True)

    name                 = models.CharField(max_length=100, null=True, blank=True)
    title                = models.CharField(max_length=255, null=True, blank=True)  
    slug                 = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description          = models.TextField(null=True, blank=True) 
    weight               = models.FloatField() 
    sku                  = models.CharField(max_length=50, unique=True, null=True, blank=True)   

    price                = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    discount_percent     = models.FloatField() 
    stock                = models.IntegerField(null=True, blank=True)

    warranty_information = models.CharField(max_length=255, null=True, blank=True) 
    shipping_information = models.CharField(max_length=255, null=True, blank=True) 
    return_policy        = models.CharField(max_length=255, null=True, blank=True)  
    min_order_quantity   = models.PositiveIntegerField(default=1)   

    unq_num              = models.CharField(default=product_unique_number, editable=False, null=True, blank=True)
    pro_uuid             = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    is_available         = models.BooleanField(default=True)
    is_approved          = models.BooleanField(default=False)

    rating               = models.FloatField(default=0.0)
    views_count          = models.PositiveIntegerField(default=0)
    sold_count           = models.PositiveIntegerField(default=0) 

    uid                  = models.CharField(max_length=255, default=product_unique_key, unique=True)


    class Meta:
        ordering = ['-created']
       

    def __str__(self) -> str:
        return f"{self.name or 'Unnamed'} - {self.price or 'N/A'} - {self.stock or 'N/A'}"
    

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            base_slug  = slugify(self.title)
            slug       = base_slug
            counter    = 1

            while ProductModel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug        = f"{base_slug}-{counter}"
                counter     += 1
            self.slug = slug

        super().save(*args, **kwargs)


    def update_stock(self, quantity: int) -> None:
        """Update the stock of the product."""
        if self.stock is None:
            raise ValueError("Stock cannot be None.")
        self.stock += quantity
        self.save()


    def reduce_stock(self, quantity: int) -> None:
        """Reduce the stock of the product."""
        if self.stock is None:
            raise ValueError("Stock cannot be None.")
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
        else:
            raise ValueError("Insufficient stock to reduce.")
        

    def restock(self, quantity: int) -> None:
        """Restock the product by a certain quantity."""
        if quantity <= 0:
            raise ValueError("Restock quantity must be positive.")
        if self.stock is None:
            raise ValueError("Stock cannot be None.")
        self.stock += quantity
        self.save()
    
    def is_product_available(self) -> bool:
        return self.is_available and (self.stock is not None and self.stock > 0)



def image_upload_to(instance, filename: str) -> str:
    """
    Generate a unique filename for the product image, organized by product and date.
    """
    ext = os.path.splitext(filename)[1].lower() or '.jpg'
    filename = f"{uuid.uuid4()}{ext}"
    product_id = instance.product.pk if instance.product else 'no_product'
    
    now = datetime.now()
    date_path = now.strftime("%Y/%m/%d")  # formats current date like '2025/05/27'

    return os.path.join(f"product_images/{product_id}", date_path, filename)




class ProductImageModel(TimeStampModel):
    """
    Model for product images, storing original and thumbnail images.
    """

    product          = models.ForeignKey(ProductModel, on_delete=models.CASCADE, null=True, blank=True, related_name="images")
    author           = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    product_image    = models.ImageField(upload_to=image_upload_to, null=True, blank=True)
    unique_id        = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_primary       = models.BooleanField(default=False)
    alt_text         = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['-created']


    def __str__(self) -> str:
        return f"{self.product.name if self.product else 'No Product'} - Image"

    def clean(self):
        """Validate image count and file extension."""
        if self.product and self.product.images.count() >= 4:
            raise ValidationError("A product can have a maximum of 4 images.")

        if self.product_image:
            ext = os.path.splitext(self.product_image.name)[1].lower()
            allowed_extensions = [".jpg", ".jpeg", ".png"]
            if ext not in allowed_extensions:
                raise ValidationError(
                    f"Unsupported file extension: {ext}. Allowed: {', '.join(allowed_extensions)}"
                )



    def make_thumbnail(self) -> InMemoryUploadedFile:
        """
        Create a thumbnail of the original image, targeting a file size under 200 KB.
        """
        try:
            with Image.open(self.product_image) as image:
                # Convert to RGB for all non-RGB images
                if image.mode != "RGB":
                    image = image.convert("RGB")

                # Resize to max 800x800, maintaining aspect ratio
                image.thumbnail((800, 800), Image.Resampling.LANCZOS)

                # Save to BytesIO with quality optimization
                image_io = BytesIO()
                quality = 95
                image.save(image_io, format="JPEG", quality=quality)

                # Optimize size if over 200 KB
                if image_io.tell() / 1024 > 200:
                    for q in range(90, 29, -5):
                        image_io = BytesIO()
                        image.save(image_io, format="JPEG", quality=q)
                        if image_io.tell() / 1024 <= 200:
                            break
                    else:
                        raise ValidationError("Could not reduce image size below 200 KB.")

                image_io.seek(0)
                return InMemoryUploadedFile(
                    image_io,
                    "ImageField",
                    f"thumb_{os.path.basename(self.product_image.name)}",
                    "image/jpeg",
                    image_io.tell(),
                    None
                )
        except UnidentifiedImageError:
            raise ValidationError("Invalid image file.")
        except Exception as e:
            raise ValidationError(f"Failed to create thumbnail: {str(e)}")

    def save(self, *args, **kwargs):
        """Override save to generate and store thumbnail."""
        self.clean()
        if self.product_image:
            self.product_image = self.make_thumbnail()
        if self.is_primary and self.product:
            ProductImageModel.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)