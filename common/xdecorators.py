from functools import wraps 
from django.http import HttpResponseForbidden 

def admin_required(view_func):
    """ """
    @wraps(view_func) 
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view 

def manager_required(view_func):
    """ """
    @wraps(view_func) 
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_manager:
            return view_func(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view 

def staff_required(view_func):
    """ """
    @wraps(view_func) 
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view 

def staff_required(view_func):
    """ """
    @wraps(view_func) 
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view 


