from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class GeneralNumberPagination(PageNumberPagination):
    page_size = 20