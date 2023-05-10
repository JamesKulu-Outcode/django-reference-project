from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from utils.paginator_meta import get_meta

class BasePaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    # max_page_size = 20
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response(get_meta(self, data))
