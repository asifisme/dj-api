from rest_framework.pagination import PageNumberPagination 


class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class that sets the default page size and maximum page size.
    """
    page_size = 20 
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_param = 'page'