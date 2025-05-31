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

from xApiProduct.models import ProductModel 
from core.xpagepagination import DynamicPagination 
from core.core_permissions import IsOwnerStaffOrSuperUser
from core.core_permissions import CartItemIsOwnerStaffOrSuperUser


class CartModelViewSet(ModelViewSet):
    """
    ViewSet for CartModel.
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
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs # if user is superuser, return all carts 
        if user.is_staff:
            return qs  # if user is staff, return all carts 
        return qs.filter(author=user) # if user is not superuser or staff, return only user's carts


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
    
    def destroy(self, request, *args, **kwargs):
        """ Override destroy method to prevent it from being used.
        """
        raise MethodNotAllowed(
            'DELETE', 
            detail="Delete operation is not allowed for CartModelViewSet.",
            code=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
   



class CartItemModelViewSet(ModelViewSet):
    """
    ViewSet for CartItemModel.
    """
    queryset                = CartItemModel.objects.all()
    serializer_class        = CartItemModelSerializer
    permission_classes      = [permissions.IsAuthenticated, CartItemIsOwnerStaffOrSuperUser]
    filter_backends        = [filters.SearchFilter, filters.OrderingFilter] 
    settings_fields          = ['product_id__uid', 'cart_id__author__username']   
    http_method_names       = ['get', 'post', 'put', 'delete'] 
    throttle_classes        = [throttling.UserRateThrottle]

    def get_queryset(self):
        user = self.request.user 

        if not user.is_authenticated:
            return CartItemModel.objects.none()

        if user.is_superuser or user.is_staff:
            return CartItemModel.objects.all() 
        
        return CartItemModel.objects.filter(cart_id__author=user)  # filter by user's cart 


    def create(self, request, *args, **kwargs):
        user = self.request.user 
        product_uid = request.data.get('product_uid')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(ProductModel, uid=product_uid)

        cart, _ = CartModel.objects.get_or_create(author=user)
        cart_item, created = CartItemModel.objects.get_or_create(
            cart_id = cart, 
            product_id = product, 

            defaults={'quantity': quantity}
        )


        if not created:
           cart_item.quantity += quantity   
           cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    



class OrderModelViewSet(ModelViewSet):
    """
    ViewSet for OrderModel.
    """
    queryset                = OrderModel.objects.all()
    serializer_class        = OrderModelSerializer
    permission_classes      = [permissions.IsAuthenticated, IsOwnerStaffOrSuperUser]
    filter_backends         = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields          = ['uid', 'author__username']   
    http_method_names       = ['get', 'post', 'put', 'delete'] 
    throttle_classes        = [throttling.UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        if user.is_staff:
            return qs
        return qs.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 
        return super().perform_create(serializer)


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
    permission_classes  = [permissions.IsAuthenticated, IsOwnerStaffOrSuperUser]
    filter_backends     = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields       = ['product_id__uid', 'order_id__author__username']   
    http_method_names   = ['get', 'post', 'put', 'delete']
    throttle_classes    = [throttling.UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        if user.is_staff:
            return qs
        return qs.filter(order_id__author=user)  # filter by user's orders