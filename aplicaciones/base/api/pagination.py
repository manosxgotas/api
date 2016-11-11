from rest_framework.pagination import PageNumberPagination


class EventoPagination(PageNumberPagination):
    page_size = 10
