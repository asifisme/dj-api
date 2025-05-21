from rest_framework.viewsets import ModelViewSet 
from rest_framework import permissions 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.exceptions import MethodNotAllowed 
from rest_framework import throttling 
from rest_framework.decorators import action 
from django.shortcuts import get_object_or_404 
from django.db import transaction 


from .models import CartModel 
from .models import CartItemModel
from .models import OrderModel
from .models import OrderItemModel  

from .serializers import CartModelSerializer
from .serializers import CartItemModelSerializer
from .serializers import OrderModelSerializer
from .serializers import OrderItemModelSerializer 

from xApiProduct.models import ProductModel 


class CartModelViewSet(ModelViewSet):
    """
    ViewSet for CartModel.
    """
    queryset                = CartModel.objects.all()
    serializer_class        = CartModelSerializer
    permission_classes      = [permissions.IsAuthenticated]
    http_method_names       = ['get', 'post', 'delete'] 
    throttle_classes        = [throttling.UserRateThrottle]


    def create(self, request, *args, **kwargs):
        """ Create a new cart for the user if it doesn't exist."""
        if 'pk' in kwargs:
            raise MethodNotAllowed(
                'POST', 
                detail="Create operation is not allowed for CartModelViewSet with a primary key.",
                code=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        # get the user from the request 
        user = self.request.user 
        existing_cart = CartModel.objects.filter(author=user).first() 
        
        # if cart exist 
        if existing_cart:
            serializer = self.get_serializer(existing_cart) 
            return Response(serializer.data, status=200) 
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user)
        return Response(serializer.data, status=201)
    


    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            'PUT', 
            detail="Update operation is not allowed for CartItemModelViewSet.",
            code=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    

    
    # not allowing update operation for cart items as per the original code logic 
    def retrieve(self, request, *args, **kwargs):
        """ Override retrieve method to prevent it from being used.
        """
        raise MethodNotAllowed(
            'GET', 
            detail="Retrieve operation is not allowed for CartModelViewSet.",
            code=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    # not allowing delete operation for cart items as per the original code logic 
    # @action(detail=False, methods=['get'], url_path='order-now')
    # def order_now(self, request):
    #     """ Handle order now action. """
    #     user = self.request.user 

    #     cart = get_object_or_404(CartModel, author=user) 
    #     cart_items = CartItemModel.objects.filter(cart_id=cart) 

    #     if not cart_items.exists():
    #         return Response({"message": "No items in the cart."}, status=status.HTTP_400_BAD_REQUEST) 
        
    #     with transaction.atomic():

    #         order_data = OrderModel.objects.create(
    #             author=user,
    #             cart_id=cart, 
    #         )

    #         order_item = [
    #             OrderItemModel(
    #                 order_id = order_data, 
    #                 product_id = item.product_id, 
    #                 quantity = item.quantity,
    #                 price = item.product_id.price * item.quantity,
    #             ) for item in cart_items 
    #         ]

    #         OrderItemModel.objects.bulk_create(order_item)  # Use bulk_create for efficiency 
    #         order_data.total_amount_calculation()  # Assuming this method exists in OrderModel to calculate total amount
    #         order_data.save()  # Save the order data after bulk_create 


    #     return Response({"message": "Order created successfully."}, status=status.HTTP_201_CREATED) 

        # order_data = OrderModel.objects.create(
        #     author=request.user,
        #     cart_id=CartModel.objects.filter(author=request.user).first(), 
        # )
        # order_data.save() 

        # cart_items = CartItemModel.objects.filter(cart_id=order_data.cart_id)
        # order_items = []
        # total_amount = 0
        # for item in cart_items:
        #     order_item = OrderItemModel.objects.create(
        #         order_id=order_data,
        #         product_id=item.product_id,
        #         quantity=item.quantity,
        #         price=item.price,
        #     )
            
        #     order_item.save()  # Moved save() call outside the loop for efficiency

        # return Response({"message": "Order now action executed."}, status=status.HTTP_200_OK)

  



class CartItemModelViewSet(ModelViewSet):
    """
    ViewSet for CartItemModel.
    """
    queryset                = CartItemModel.objects.all()
    serializer_class        = CartItemModelSerializer
    permission_classes      = [permissions.AllowAny]
    http_method_names       = ['get', 'post', 'put', 'delete'] 
    throttle_classes        = [throttling.UserRateThrottle]


    def create(self, request, *args, **kwargs):
        user = self.request.user 
        product_uid = request.data.get('product_uid')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(ProductModel, uid=product_uid)

        cart, _ = CartModel.objects.get_or_create(author=user)
        cart_item, created = CartItemModel.objects.get_or_create(
            cart_id = cart, 
            product_id = product, 
            defaults={
                'quantity' : quantity,
                'price': product.price * quantity, 
            }
        )


        if not created:
           cart_item.quantity += quantity  # corrected variable name
           cart_item.price = product.price * cart_item.quantity  
           cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def update(self, request, *args, **kwargs):
        """ Update an existing cart item. """
        cart_item = get_object_or_404(CartItemModel, pk=kwargs['pk'])
        quantity = int(request.data.get('quantity', cart_item.quantity))
        cart_item.quantity = quantity
        cart_item.price = cart_item.product.price * quantity
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)





class OrderModelViewSet(ModelViewSet):
    """
    ViewSet for OrderModel.
    """
    queryset                = OrderModel.objects.all()
    serializer_class        = OrderModelSerializer
    permission_classes      = [permissions.IsAuthenticated]
    http_method_names       = ['get', 'post', 'put', 'delete'] 
    throttle_classes        = [throttling.UserRateThrottle]


    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            'PUT', 
            detail="Update operation is not allowed for OrderModelViewSet.",
            code=status.HTTP_405_METHOD_NOT_ALLOWED
        )





class OrderItemModelViewSet(ModelViewSet):
    """
    ViewSet for OrderItemModel.
    """
    queryset            = OrderItemModel.objects.all()
    serializer_class    = OrderItemModelSerializer
    permission_classes  = [permissions.IsAuthenticated]
    http_method_names   = ['get', 'post', 'put', 'delete']
    throttle_classes    = [throttling.UserRateThrottle]