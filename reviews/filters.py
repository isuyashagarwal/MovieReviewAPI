import django_filters
from .models import Review

class ReviewFilter(django_filters.FilterSet):
    movie_title = django_filters.CharFilter(field_name='movie__title', lookup_expr='icontains')
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    rating = django_filters.NumberFilter(field_name='rating')

    class Meta:
        model = Review
        fields = ['movie_title', 'user', 'rating']