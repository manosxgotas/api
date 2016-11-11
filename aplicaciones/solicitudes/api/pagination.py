from rest_framework.pagination import PageNumberPagination


class SolicitudDonacionPagination(PageNumberPagination):
    page_size = 10
