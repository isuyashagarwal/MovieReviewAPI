from django.urls import path
from .views import get_movie, list_movies, get_movie_reviews

urlpatterns = [
    path('<str:title>/', get_movie, name='get_movie'),
    path('', list_movies, name='list_movies'),
    path('<int:movie_id>/reviews/', get_movie_reviews, name='get_movie_reviews'),
]