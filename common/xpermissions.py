from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    """Base permission class for checking user roles."""
    required_role = None

    def has_permission(self, request, view):
        """ Check if the user has the required role for the view.""" 
        return (
            request.user.is_authenticated and
            getattr(request.user, self.required_role, False)
        )

    def has_object_permission(self, request, view, obj):
        """ Check if the user has the required role for the object.""" 
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'user', None) == request.user


class IsAdmin(RoleBasedPermission):
    """Allows access only to admin users."""
    required_role = 'is_admin'


class IsManager(RoleBasedPermission):
    """Allows access only to manager users."""
    required_role = 'is_manager'


class IsStaff(RoleBasedPermission):
    """Allows access only to staff users."""
    required_role = 'is_staff'


class IsEditor(RoleBasedPermission):
    """Allows access only to editor users."""
    required_role = 'is_editor'
