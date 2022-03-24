from django_filters import rest_framework
from django_filters.filters import CharFilter, NumberFilter

from reviews.models import Title


class TitleFilterSet(rest_framework.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberFilter(field_name='year', lookup_expr='exact')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
