from rest_framework import viewsets 
from rest_framework import permissions 
from django.contrib.auth import get_user_model 

from .serializers import UserProfileSerializer 
from core.pagepagination import DynamicPagination 
from core.core_permissions import IsOwnerStaffOrSuperUser 


User = get_user_model()

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() 
    serializer_class    = UserProfileSerializer 
    permission_classes = [permissions.IsAuthenticated, IsOwnerStaffOrSuperUser] 
    pagination_class   = DynamicPagination 

    def get_queryset(self):
        user = self.request.user 
        qs =  super().get_queryset()

        if user.is_superuser or user.is_staff:
            return qs 
        
        return qs.filter(pk=user.pk)
        
    

