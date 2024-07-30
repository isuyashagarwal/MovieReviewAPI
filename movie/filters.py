import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    release_date = django_filters.DateFilter(field_name='release_date')

    class Meta:
        model = Movie
        fields = ['title', 'release_date']