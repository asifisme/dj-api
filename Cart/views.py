from rest_framework.viewsets import ModelViewSet 
from rest_framework import permissions 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.exceptions import MethodNotAllowed 
from rest_framework import throttling 
from rest_framework import filters 


from rest_framework.decorators import action 
from django.shortcuts import get_object_or_404 
from decimal import Decimal 


from .models import CartModel 
from .models import CartItemModel
from .models import OrderModel
from .models import OrderItemModel  

from .serializers import CartModelSerializer
from .serializers import CartItemModelSerializer
from .serializers import OrderModelSerializer
from .serializers import OrderItemModelSerializer 

from Product.models import ProductModel 
from core.pagepagination import DynamicPagination 
from core.core_permissions import IsOwnerStaffOrSuperUser
from core.core_permissions import CartItemIsOwnerStaffOrSuperUser




class CartModelViewSet(ModelViewSet):
    """
    ViewSet for CartModel.
    Handles all cart-related API operations, including listing, creating, and retrieving carts.
    Enforces permissions so that only authenticated users can access their own carts, while staff and superusers have broader access.
    Implements search and pagination for efficient cart management.
    """
    queryset                = CartModel.objects.all()
    serializer_class        = CartModelSerializer
    permission_classes      = [permissions.IsAuthenticated, IsOwnerStaffOrSuperUser] 
    filter_backends         = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields          = ['uid', 'author__username']  # allow searching by uid and author's username 
    http_method_names       = ['get', 'post'] 
    throttle_classes        = [throttling.UserRateThrottle]
    pagination_class        = DynamicPagination  
 

    def get_queryset(self):
        """
        Returns the queryset of CartModel objects accessible to the current user.
        - Superusers and staff can access all carts.
        - Regular users only see their own carts.
        This enforces data privacy and access control at the API level.
        """
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs # if user is superuser, return all carts 
        if user.is_staff:
            return qs  # if user is staff, return all carts 
        return qs.filter(author=user) # if user is not superuser or staff, return only user's carts


    def create(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new cart for the authenticated user.
        Ensures only one active cart per user, returning the existing cart if found.
        Validates input and provides clear, structured API responses for all outcomes.
        """
        if 'pk' in kwargs:
            raise MethodNotAllowed(
                'POST',
                detail="Create operation is not allowed for CartModelViewSet with a primary key.",
                code=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        user = self.request.user
        existing_cart = CartModel.objects.filter(author=user).first()

        if existing_cart:
            serializer = self.get_serializer(existing_cart)
            return Response({ "message": "Cart already exists for this user.", "cart": serializer.data }, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user)

        return Response({"message": "Cart created successfully.", "cart": serializer.data}, status=status.HTTP_201_CREATED)
    


    def update(self, request, *args, **kwargs):
        """
        Disables the update operation for CartModelViewSet by raising MethodNotAllowed.
        This enforces business rules that carts cannot be updated via this endpoint.
        """
        raise MethodNotAllowed(
            'PUT',
            detail="Update operation is not allowed for CartItemModelViewSet.",
            code=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
  
    def destroy(self, request, *args, **kwargs):
        """
        Disables the destroy operation for CartModelViewSet by raising MethodNotAllowed.
        This prevents deletion of carts via the API, preserving data integrity.
        """
        raise MethodNotAllowed(
            'DELETE',
            detail="Delete operation is not allowed for CartModelViewSet.",
            code=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
   



class CartItemModelViewSet(ModelViewSet):
    """
    ViewSet for CartItemModel.
    Handles all cart item-related API operations, including adding, updating, and removing items from a user's cart.
    Enforces permissions so that only the cart owner, staff, or superusers can modify cart items.
    Provides search and filtering capabilities for efficient cart item management.
    """
    queryset                = CartItemModel.objects.all()
    serializer_class        = CartItemModelSerializer
    permission_classes      = [permissions.IsAuthenticated, CartItemIsOwnerStaffOrSuperUser]
    filter_backends        = [filters.SearchFilter, filters.OrderingFilter] 
    settings_fields          = ['product_id__uid', 'cart_id__author__username']   
    http_method_names       = ['get', 'post', 'put', 'delete'] 
    throttle_classes        = [throttling.UserRateThrottle]

    def get_queryset(self):
        """
        Returns the queryset of CartItemModel objects accessible to the current user.
        - Superusers and staff can access all cart items.
        - Regular users only see items in their own carts.
        Ensures data privacy and correct access control.
        """
        user = self.request.user 

        if not user.is_authenticated:
            return CartItemModel.objects.none()

        if user.is_superuser or user.is_staff:
            return CartItemModel.objects.all() 
        
        return CartItemModel.objects.filter(cart_id__author=user)  # filter by user's cart 


    def create(self, request, *args, **kwargs):
        """
        Handles POST requests to add a product to the user's cart.
        If the product already exists in the cart, increments the quantity.
        Returns a clear message and the updated or created cart item.
        """
        user = self.request.user
        product_uid = request.data.get('product_uid')

        delta = int(request.data.get('quantity', 1))

        if delta == 0:
            return Response({
                "error": "Quantity must be greater than zero.",
                "message": "Please provide a valid quantity to add to the cart."
            }, status=status.HTTP_400_BAD_REQUEST) 


        product = get_object_or_404(ProductModel, uid=product_uid)
        cart, _ = CartModel.objects.get_or_create(author=user)

        try:
            cart_item = CartItemModel.objects.get(cart_id=cart, product_id=product)
            new_quantity = cart_item.quantity + delta

            if new_quantity < 1:
                cart_item.delete()
                return Response({
                    "message": "Item removed from cart because quantity dropped to zero."
                }, status=status.HTTP_200_OK)

            cart_item.quantity = new_quantity
            cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response({
                "message": "Cart item quantity updated.",
                "cart_item": serializer.data
            }, status=status.HTTP_200_OK)
        except CartItemModel.DoesNotExist:
            if delta < 1:
                return Response({
                    "error": "Cannot reduce quantity below 1. Item not in cart."
                }, status=status.HTTP_400_BAD_REQUEST)

            cart_item = CartItemModel.objects.create(
                cart_id=cart,
                product_id=product,
                quantity=delta
            )
            serializer = self.get_serializer(cart_item)
            return Response({
                "message": "Cart item added successfully.",
                "cart_item": serializer.data
            }, status=status.HTTP_201_CREATED)
    
    


class OrderModelViewSet(ModelViewSet):
    """
    ViewSet for OrderModel.
    Handles all order-related API operations, including creating, listing, and retrieving orders.
    Enforces permissions so that only authenticated users can access their own orders, while staff and superusers have broader access.
    Implements search and pagination for efficient order management.
    """
    queryset                = OrderModel.objects.all()
    serializer_class        = OrderModelSerializer
    permission_classes      = [permissions.IsAuthenticated, IsOwnerStaffOrSuperUser]
    filter_backends         = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields          = ['uid', 'author__username']   
    http_method_names       = ['get', 'post', 'put', 'delete'] 
    throttle_classes        = [throttling.UserRateThrottle]

    def get_queryset(self):
        """
        Returns the queryset of OrderModel objects accessible to the current user.
        - Superusers and staff can access all orders.
        - Regular users only see their own orders.
        This enforces data privacy and access control at the API level.
        """
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        if user.is_staff:
            return qs
        return qs.filter(author=user)
    
    def create(self, request, *args, **kwargs):
        """ 
        Handles POST requests to create a new order for the authenticated user.
        - Checks if the user has confirmed the order to prevent accidental orders.
        - Validates that the user has no existing incomplete orders.
        - Ensures the user has an active cart with items before creating an order.
        - Transfers items from the user's cart to the new order.
        - Returns a structured response with order details upon successful creation.
        """
        user = request.user
        # Check if the user has confirmed the order (prevents accidental orders)
        is_confirm = request.data.get('is_confirm', False)
        if not is_confirm:
            # Return error if order is not confirmed
            return Response(
                {
                    "error": "Order confirmation required.",
                    "message": "Please confirm the order before placing it."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Check for any existing incomplete order for the user
        incomplate_order = OrderModel.objects.filter(author=user).exclude(ord_status='completed').first()
        if incomplate_order:
            # Return error if there is an incomplete order
            return Response(
                {
                    "error": "Previous order incomplete.",
                    "message": "You cannot create a new order until your previous order is completed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Get the user's active cart
        cart = CartModel.objects.filter(author=user).first()
        if not cart:
            # Return error if no active cart is found
            return Response(
                {
                    "error": "No active cart found.",
                    "message": "You do not have an active cart. Please add items to your cart before placing an order."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Get all items in the user's cart
        cart_items = CartItemModel.objects.filter(cart_id=cart)
        if not cart_items.exists():
            # Return error if the cart is empty
            return Response(
                {
                    "error": "Cart is empty.",
                    "message": "No items in the cart. Please add products to your cart before placing an order."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Create a new order for the user
        order_data = OrderModel.objects.create(
            author=user,
            cart_id=cart,
        )
        order_data.save()
        # Move each cart item to the new order as an order item
        for item in cart_items:
            order_item = OrderItemModel.objects.create(
                order_id=order_data,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            order_item.save()
        # Clear the cart after transferring items
        cart_items.delete()
        # Return success response with order details
        return Response({
            'message': 'Order created successfully.',
            'order_id': order_data.id,
            'total_amount': order_data.total_amount,
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """ 
        Custom save method for OrderModelViewSet.
        - Automatically sets the author of the order to the current user.
        - Associates the order with the user's active cart.
        - Ensures the order is created with the correct author and cart association.
        """
        user = self.request.user
        cart = CartModel.objects.filter(author=user).first()
        serializer.save(author=user, cart_id=cart)
        return super().perform_create(serializer)

    def update(self, request, *args, **kwargs):
        """
        Disables the update operation for OrderModelViewSet by raising MethodNotAllowed.
        This enforces business rules that orders cannot be updated via this endpoint.
        """
        raise MethodNotAllowed(
            'PUT', 
            detail="Update operation is not allowed for OrderModelViewSet.",
            code=status.HTTP_405_METHOD_NOT_ALLOWED
        )





class OrderItemModelViewSet(ModelViewSet):
    """
    ViewSet for OrderItemModel.
    Handles all order item-related API operations, including listing and retrieving items in a user's orders.
    Enforces permissions so that only the order owner, staff, or superusers can access order items.
    Provides search and filtering capabilities for efficient order item management.
    """
    queryset            = OrderItemModel.objects.all()
    serializer_class    = OrderItemModelSerializer
    permission_classes  = [permissions.IsAuthenticated, IsOwnerStaffOrSuperUser]
    filter_backends     = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields       = ['product_id__uid', 'order_id__author__username']   
    http_method_names   = ['get', 'post', 'put', 'delete']
    throttle_classes    = [throttling.UserRateThrottle]

    def get_queryset(self):
        """
        Returns the queryset of OrderItemModel objects accessible to the current user.
        - Superusers and staff can access all order items.
        - Regular users only see items in their own orders.
        Ensures data privacy and correct access control.
        """
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        if user.is_staff:
            return qs
        return qs.filter(order_id__author=user)  # filter by user's orders