


import uuid
import logging
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .models import JournalEntryModel
from .serializers import JournalEntrySerializer
from .permissions import IsOwnerOrReadOnly
from appAccount.models import AccountModel
from appEmployee.models import EmployeeModel

# from appAccount.paginations import StanderdResultsSetPagination 
from rest_framework.pagination import PageNumberPagination 

class StanderdResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_query_param = 'page'

Entry = JournalEntryModel 


logger = logging.getLogger(__name__)

PERSMISSION_CONTROLLER = [permissions.AllowAny]

class JournalEntryViewSet(ModelViewSet):
    queryset = JournalEntryModel.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = PERSMISSION_CONTROLLER
    pagination_class   = StanderdResultsSetPagination 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        cleaned_data = serializer.validated_data

        # Extract serializer fields
        ent_name = cleaned_data.get('ent_name', '').strip()
        ent_description = cleaned_data.get('ent_description', '').strip()
        amount = cleaned_data.get('amount', 0)
        is_cash_transaction = cleaned_data.get('cash', True)
        category = cleaned_data.get('category', '')


        if amount <= 0 or not amount:
            return Response({
                'errors': 'Amount must be greater than zero'
            }, status=status.HTTP_400_BAD_REQUEST) 
        
        if not category or category not in Entry.CATEGORY.values:
            return Response({
                'errors': 'Invalid category'
            }, status=status.HTTP_400_BAD_REQUEST) 


        try:
            with transaction.atomic():
                # Generate unique transaction numbers
                category_list = Entry.CATEGORY # shotcut for category list 
                cash_balane = 'cash_balance'
                bank_balance = 'bank_balance'

                # Determine debit and credit names
                if category == category_list.SALES_REVENUE:
                    debit_name =  cash_balane if is_cash_transaction == True else bank_balance
                    credit_name = "sales revenue"
                    
                elif category == category_list.SERVICE_REVENUE:
                    debit_name =  cash_balane if is_cash_transaction == True else bank_balance
                    credit_name = "sales_revenue"

                elif category == category_list.INTEREST_EARNED:
                    debit_name =  cash_balane if is_cash_transaction == True else bank_balance 
                    credit_name = "service_revenue"
                    
                elif category ==  category_list.PURCHASES:
                    debit_name = "purchases"
                    credit_name = cash_balane if is_cash_transaction == True else bank_balance 

                elif category == category_list.RENT_EXPENSE:
                    debit_name = "rent_expense"
                    credit_name = cash_balane if is_cash_transaction == True else bank_balance 

                elif category == category_list.SALARY_PAYMENT:
                    debit_name = "salary_payment"
                    credit_name = cash_balane if is_cash_transaction == True else bank_balance

                elif category == category_list.UTILITY_BILLS:
                    debit_name = "utility_bills"
                    credit_name = cash_balane if is_cash_transaction == True else bank_balance 

                elif category == category_list.TRAVEL_EXPENSE:
                    debit_name = "travel_expense"
                    credit_name = cash_balane if is_cash_transaction == True else bank_balance 

                elif category == category_list.MAINTENANCE_COST:
                    debit_name = "maintenance_cost"
                    credit_name = cash_balane if is_cash_transaction == True else bank_balance 

                elif category == category_list.OFFICE_SUPPLIES:
                    debit_name = "office_supplies"
                    credit_name = cash_balane if is_cash_transaction == True else bank_balance 

                elif category == category_list.MARKETING_ADS:
                    debit_name = "marketing_ads"
                    credit_name = cash_balane if is_cash_transaction == True else bank_balance

                elif category == category_list.BANK_CHARGES:
                    debit_name = "bank_charges" 
                    credit_name = cash_balane if is_cash_transaction == True else bank_balance 

                elif category == category_list.CASH_IN_HAND:
                    debit_name = "cash_in_hand"
                    credit_name = cash_balane if is_cash_transaction == True else bank_balance 

                elif category == category_list.ACCOUNTS_RECEIVABLE:
                    debit_name = cash_balane if is_cash_transaction == True else bank_balance 
                    credit_name = "accounts_receivable" 

                elif category == category_list.ACCOUNTS_PAYABLE:
                    debit_name  =  cash_balane if is_cash_transaction == True else bank_balance
                    credit_name = "accounts_payable" 
                

                # Create journal entry
                journal_entry = Entry.objects.create(
                    ent_name        = ent_name,
                    ent_description = ent_description,
                    amount          = amount,
                    category        = category,
                    debit           = amount,
                    credit          = amount,
                    debit_name      = debit_name,
                    credit_name     = credit_name,
                    user            = request.user if request.user.is_authenticated else None,
                )

                return Response({
                    'message': 'Journal entry created successfully',
                    'data': self.get_serializer(journal_entry).data
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating journal entry: {str(e)}")
            return Response({
                'errors': f"Failed to create journal entry: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)