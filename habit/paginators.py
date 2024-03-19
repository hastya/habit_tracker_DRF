from rest_framework.pagination import PageNumberPagination


class ReflexPagination(PageNumberPagination):
    page_size = 10
