from rest_framework.pagination import PageNumberPagination 


class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class that sets the default page size and maximum page size.
    """
    page_size = 20 
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_param = 'page'



from rest_framework.pagination import PageNumberPagination 
from rest_framework.pagination import  LimitOffsetPagination
from rest_framework.pagination import CursorPagination 
from rest_framework.pagination import  BasePagination
from rest_framework.response import Response

class StandardPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 1000
    page_query_param = 'page'
    page_size_query_param = 'size'


class StandardLimitPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100


class StandardCursorPagination(CursorPagination):
    page_size           = 100 
    ordering            = '-created_at' 
    offset_query_param  = 'offset'


class DynamicPagination(BasePagination):
    def paginate_queryset(self, queryset, request, view=None):
        pagination_type = request.query_params.get('pagination', 'page')

        if pagination_type == 'limit':
            self.paginator = StandardLimitPagination()
        else:
            self.paginator = StandardPagination()

        return self.paginator.paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)



# from rest_framework.pagination import (
#     PageNumberPagination,
#     LimitOffsetPagination,
#     CursorPagination,
#     BasePagination
# )
# from rest_framework.response import Response


# class StandardPagination(PageNumberPagination):
#     page_size = 10
#     max_page_size = 100
#     page_query_param = 'page'
#     page_size_query_param = 'size'


# class StandardLimitPagination(LimitOffsetPagination):
#     default_limit = 10
#     max_limit = 100
#     limit_query_param = 'limit'
#     offset_query_param = 'offset'


# class StandardCursorPagination(CursorPagination):
#     page_size = 10
#     ordering = '-created_at'  # Change this to your timestamp field
#     cursor_query_param = 'cursor'


# class DynamicPagination(BasePagination):
#     def paginate_queryset(self, queryset, request, view=None):
#         self.request = request
#         pagination_type = request.query_params.get('pagination', 'page')

#         if pagination_type == 'limit':
#             self.paginator = StandardLimitPagination()
#         elif pagination_type == 'cursor':
#             self.paginator = StandardCursorPagination()
#         else:
#             self.paginator = StandardPagination()

#         return self.paginator.paginate_queryset(queryset, request, view=view)

#     def get_paginated_response(self, data):
#         # Handle custom response formats for each type
#         paginator = self.paginator

#         if isinstance(paginator, PageNumberPagination):
#             return Response({
#                 "type": "page",
#                 "count": paginator.page.paginator.count,
#                 "current_page": paginator.page.number,
#                 "next": paginator.get_next_link(),
#                 "previous": paginator.get_previous_link(),
#                 "results": data
#             })

#         elif isinstance(paginator, LimitOffsetPagination):
#             return Response({
#                 "type": "limit",
#                 "count": paginator.count,
#                 "limit": paginator.get_limit(self.request),
#                 "offset": paginator.get_offset(self.request),
#                 "next": paginator.get_next_link(),
#                 "previous": paginator.get_previous_link(),
#                 "results": data
#             })

#         elif isinstance(paginator, CursorPagination):
#             return Response({
#                 "type": "cursor",
#                 "next": paginator.get_next_link(),
#                 "previous": paginator.get_previous_link(),
#                 "results": data
#             })

#         return Response({
#             "results": data
#         })
