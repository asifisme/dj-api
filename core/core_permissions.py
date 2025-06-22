from rest_framework.permissions import BasePermission 
from rest_framework.permissions import SAFE_METHODS 


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    All other users can only read (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
       # super user can do anything 
        if request.user and request.user.is_superuser:
           return True 
        
        # Safe methods (GET, HEAD, OPTIONS) are allowed for all users. 
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object. 
        return obj.author == request.user




class IsOwnerStaffOrSuperUser(BasePermission):
      """
      Only the object owner has full access.
      Staff can only read (GET).
      Superuser can do everything.
      All other users are denied.
      """

      def has_object_permission(self, request, view, obj):
         # Superuser can do anything 
         if request.user.is_authenticated and (request.user and request.user.is_superuser):
               return True
         
         # Staff can do only (GET) 
         if request.user.is_authenticated and (request.user and request.user.is_staff):
               return request.method in SAFE_METHODS
         
         # Owner can do anything 
         if obj == request.user:
               return True
         
         # Deny all other users
         return False 




class CartItemIsOwnerStaffOrSuperUser(BasePermission):
    """
    Custom permission to only allow the owner, staff, or superuser to access the view.
    """

    def has_object_permission(self, request, view, obj):
        # Superuser can do anything 
        if request.user.is_authenticated and (request.user and request.user.is_superuser):
            return True 
        
        # Staff can do only (GET) 
        if request.user.is_authenticated and (request.user and request.user.is_staff):
            return request.method in SAFE_METHODS
        
        # Owner can do anything 
        if obj.cart_id.author == request.user:
            return True
        
        # Deny all other users
        return False
  



class IsSuperUser(BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """

    def has_permission(self, request, view):
        # Allow access only if the user is authenticated and is a superuser
        return request.user.is_authenticated and request.user.is_superuser 
    



class IsStaffOrReadOnly(BasePermission):
    """
    Custom permission to only allow staff members to edit the object.
    All other users can only read (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # Superuser can do anything 
        if request.is_authenticated and (request.user and request.user.is_superuser):
            return True 
        
        # Staff can do anything 
        if request.is_authenticated and (request.user and request.user.is_staff):
            return True 
        
        # Safe methods (GET, HEAD, OPTIONS) are allowed for all users. 
        if request.is_authenticated and (request.method in SAFE_METHODS):
            return True
        
        # Deny all other users
        return False 
    



class IsAuthenticated(BasePermission):
    """
    Custom permission to only allow authenticated users to access the view.
    """

    def has_permission(self, request, view):
        # Allow access only if the user is authenticated
        return request.user.is_authenticated 
    



class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to only allow authenticated users to edit the object.
    All other users can only read (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated or if the method is safe
        return request.user.is_authenticated or request.method in SAFE_METHODS
    



class IsAuthenticatedOrOwner(BasePermission):
    """
    Custom permission to only allow authenticated users or the owner of the object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow access if the user is authenticated
        if request.user.is_authenticated:
            return True
        
        # Allow access if the user is the owner of the object
        return obj.owner == request.user  
    



class IsAuthenticatedOrStaff(BasePermission):
    """
    Custom permission to only allow authenticated users or staff members to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated
        if request.user.is_authenticated:
            return True
        
        # Allow access if the user is a staff member
        return request.user.is_staff 
    



class IsAuthenticatedOrSuperUser(BasePermission):
    """
    Custom permission to only allow authenticated users or superusers to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated
        if request.user.is_authenticated:
            return True
        
        # Allow access if the user is a superuser
        return request.user.is_superuser 
    



class IsAuthenticatedOrStaffOrSuperUser(BasePermission): 
    """
    Custom permission to only allow authenticated users, staff members, or superusers to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated
        if request.user.is_authenticated:
            return True
        
        # Allow access if the user is a staff member
        if request.user.is_staff:
            return True
        
        # Allow access if the user is a superuser
        return request.user.is_superuser