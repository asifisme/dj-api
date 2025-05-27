import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from xApiProduct.models import ProductModel, ProductImageModel
from xApiAuthentication.models import CustomUser as User 

class Command(BaseCommand):
    help = "Attach one image to each product from fixtures/media/products with author ID 1001"

    def handle(self, *args, **kwargs):
        media_dir = os.path.join(settings.BASE_DIR, "xApi/fixtures/media/products")
        all_images = sorted([
            f for f in os.listdir(media_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])

        products = ProductModel.objects.all().order_by('id')
        total_products = products.count()
        total_images = len(all_images)

        if total_images < total_products:
            self.stdout.write(self.style.ERROR(f"❌ Not enough images: {total_images} images for {total_products} products."))
            return

        try:
            author = User.objects.get(pk=1001)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ User with ID 1001 not found."))
            return

        for product, image_name in zip(products, all_images):
            image_path = os.path.join(media_dir, image_name)

            with open(image_path, 'rb') as f:
                image_file = File(f)
                img = ProductImageModel(
                    product=product,
                    author=author,
                    product_image=image_file,
                    is_primary=True,
                    alt_text=f"Image of {product.name}"
                )
                img.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Linked {image_name} -> {product.name}"))

        self.stdout.write(self.style.SUCCESS(f"\n🎯 All done! {total_products} products linked with images."))
