from django.db import models 
from rest_framework import viewsets 
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import permissions 
from rest_framework import throttling 

from core.core_permissions import IsOwnerStaffOrSuperUser 

from .models import JournalEntryModel 
from .serializers import TrialBalanceSerializer 



class TrialBalanceViewSet(APIView):
    # permission_classes = [permissions.IsAuthenticated, IsOwnerStaffOrSuperUser]  
    serializer_class = TrialBalanceSerializer 

    def post(self, request, *args, **kwargs):
        """
        Example endpoint to demonstrate trial balance calculation.
        This can be extended to filter by date range or other parameters.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data.get('created')
        ended = serializer.validated_data.get('ended')

        if not start_date or not ended:
            return Response({"error": "Both 'created' and 'ended' dates are required."}, status=400)
        
        total_debit = JournalEntryModel.objects.filter(status='posted', created__gte=start_date, created__lte=ended).aggregate(total_debit=models.Sum('debit_amount'))['total_debit'] or 0
        total_credit = JournalEntryModel.objects.filter(status='posted', created__gte=start_date, created__lte=ended).aggregate(total_credit=models.Sum('credit_amount'))['total_credit'] or 0
        
        trial_balance = {
            'total_debit': total_debit,
            'total_credit': total_credit,
            'balance': total_debit - total_credit
        }
        
        return Response(trial_balance)
    
