from django_filters import rest_framework as filters
from .models import Book


class BookFilter(filters.FilterSet):
    min_date = filters.DateFilter(field_name="publish_date", lookup_expr="gte")
    max_date = filters.DateFilter(field_name="publish_date", lookup_expr="lte")
    genre = filters.CharFilter(field_name="genre__name")
    author = filters.CharFilter(field_name="author__last_name")

    class Meta:
        model = Book
        fields = ["genre", "author", "min_date", "max_date"]
