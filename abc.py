import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xApi.settings")
django.setup()

from xApiCart.models import OrderModel

# Remove duplicates for a specific order_num
order_num = 1000000000
orders = OrderModel.objects.filter(order_num=order_num).order_by('-id')
to_keep = orders.first()
to_delete = orders[1:]

print(f"Keeping: {to_keep}")
for order in to_delete:
    try:
        print(f"Deleting: {order}")
        order.delete()
    except Exception as e:
        print(f"Failed to delete {order}: {e}")


