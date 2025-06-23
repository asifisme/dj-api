import controller 
from rest_framework import viewsets 
from rest_framework import permissions 
from rest_framework.response import Response 
from rest_framework import status 

from django.contrib.auth import get_user_model 
from django.core.mail import send_mail 
from django.conf import settings 

from .serializers import UserProfileSerializer
from .serializers import MaiTablelSerializer 
from .models import MailTable 

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
        


    
class SendMailViewSet(viewsets.ModelViewSet):
    queryset         = MailTable.objects.all()
    serializer_class = MaiTablelSerializer
    permission_classes  = [permissions.IsAuthenticated, IsOwnerStaffOrSuperUser] 
    pagination_class = DynamicPagination 

    def create(self, request):
        seriliser = self.get_serializer(data=request.data)

        if not seriliser.is_valid():
            return Response({"message" : "Serializer is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        subject         = seriliser.validated_data['subject']
        message         = seriliser.validated_data['message']
        to_email        = seriliser.validated_data['to_email'] 

        try:
            if controller.GLOBAL_EMAIL_SYSTEM:
                send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[to_email], fail_silently=False )
                seriliser.save(
                    author=self.request.user,
                    status='sent')
            return Response({"success": "Mail has been successfully send"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        user = self.request.user 
        qs = super().get_queryset()

        if user.is_superuser or user.is_staff:
            return qs 
        
        return qs.filter(author=user)