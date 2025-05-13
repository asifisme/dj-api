import os
import uuid
import sys
from io import BytesIO
from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError

User = get_user_model()


class TimeStampModel(models.Model):
    """
    Abstract base class that provides self-updating 'created' and 'modified' fields.
    """
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def product_categor_unique_key()-> str:
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
    uid    = models.CharField(max_length=255, default=product_categor_unique_key, null=True, blank=True)

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
    author          = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    uid        = models.CharField(max_length=255, default=product_meta_tag_unique_key, null=True, blank=True)

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
    cate        = models.ForeignKey(ProductCategoryModel, on_delete=models.PROTECT, null=True, blank=True)
    author      = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    meta_tag    = models.ForeignKey(ProductMetaTagModel, on_delete=models.PROTECT, null=True, blank=True)
    name        = models.CharField(max_length=100, null=True, blank=True)
    title       = models.CharField(max_length=255, null=True, blank=True)
    slug        = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    desc        = models.TextField(null=True, blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock       = models.IntegerField(null=True, blank=True)
    unq_num     = models.CharField(default=product_unique_number, editable=False, null=True, blank=True)
    available   = models.BooleanField(default=True)
    approve     = models.BooleanField(default=False)
    pro_uuid    = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    uid     = models.CharField(max_length=255, default=product_unique_key, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name or 'Unnamed'} - {self.price or 'N/A'} - {self.stock or 'N/A'}"

    def save(self, *args, **kwargs):
        if not self.unq_num:
            self.unq_num = product_unique_number()

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

    def is_available(self) -> bool:
        """Check if the product is available."""
        return self.available and (self.stock is not None and self.stock > 0)

    def get_price(self):
        """Get the price of the product."""
        return self.price

    def is_approved(self) -> bool:
        """Check if the product is approved."""
        return self.approve


def image_upload_to(instance, filename: str) -> str:
    """
    Generate a unique filename for the product image.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(f"product_{instance.product.pk}", "images", filename)


class ProductImageModel(TimeStampModel):
    """
    Model for product images.
    """
    product     = models.ForeignKey(ProductModel, on_delete=models.CASCADE, null=True, blank=True, related_name="images")
    author      = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    image       = models.ImageField(upload_to=image_upload_to, null=True, blank=True)
    uid     = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        return f"{self.product or 'No Product'} - Image"

    def make_thumbnail(self):
        """
        Create a thumbnail of the image.
        """
        try:
            image = Image.open(self.image)
            image.thumbnail((800, 800))

            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            image_io = BytesIO()
            quality = 95
            while quality >= 30:
                image_io.seek(0)
                image_io.truncate()
                image.save(image_io, format="JPEG", quality=quality)
                size_kb = image_io.tell() / 1024
                if size_kb < 200:
                    break
                quality -= 5

            image_io.seek(0)
            return image_io

        except Exception as e:
            raise ValidationError(f"Thumbnail Error: {e}")

    def save(self, *args, **kwargs):
        """Override the save method to perform custom actions."""
        if self.product and self.product.images.count() >= 4:
            raise ValueError("A product can have a maximum of 4 images.")

        if self.image:
            ext = os.path.splitext(self.image.name)[1].lower()
            allowed_extensions = [".jpg", ".jpeg", ".png"]
            if ext not in allowed_extensions:
                raise ValidationError(f"Unsupported file extension: {ext}. Allowed extensions are: {allowed_extensions}")

            thumb = self.make_thumbnail()
            if thumb:
                self.image = InMemoryUploadedFile(
                    thumb,
                    "ImageField",
                    self.image.name,
                    "image/jpeg",
                    sys.getsizeof(thumb),
                    None
                )

        super().save(*args, **kwargs)