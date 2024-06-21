from rest_framework.pagination import PageNumberPagination


class HabitsPagination(PageNumberPagination):
    """ Пагинация на 5 обьектов в страничке """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
