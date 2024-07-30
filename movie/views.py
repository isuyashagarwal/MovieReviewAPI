from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
import requests
from django.conf import settings
from .models import Movie
from .serializers import MovieSerializer
from .filters import MovieFilter
from reviews.filters import ReviewFilter
from reviews.models import Review
from reviews.serializers import ReviewSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def get_movie(request, title):
    """
    Gets movie from TMDb API if it does not exist in database.

    Args:
    Movie Title.

    Returns:
    Response: Movie Details - Title, description, release date and poster.
    """

    try:
        movie = Movie.objects.get(title__iexact=title)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query={title}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                movie_data = data['results'][0]
                movie = Movie.objects.create(
                    title=movie_data['title'],
                    description=movie_data['overview'],
                    release_date=movie_data['release_date'],
                    poster=f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}"
                )
                serializer = MovieSerializer(movie)
                return Response(serializer.data)
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Failed to fetch data from TMDb"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def list_movies(request):
    """
    List all movies with search, filter, and pagination functionality.

    Returns:
    Response: A paginated list of movies.
    """
    movies = Movie.objects.all()

    filtered_queryset = MovieFilter(request.GET, queryset=movies).qs

    paginator = StandardResultsSetPagination()
    paginated_queryset = paginator.paginate_queryset(filtered_queryset, request)

    serializer = MovieSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def get_movie_reviews(request, movie_id):
    """
    Retrieve reviews for a specific movie by movie ID.

    Args:
    movie_id (int): The ID of the movie to retrieve reviews for.

    Returns:
    Response: A paginated list of reviews for the specified movie.
    """
    try:
        movie = Movie.objects.get(id=movie_id)
        reviews = Review.objects.filter(movie=movie)
        filtered_queryset = ReviewFilter(request.GET, queryset=reviews).qs

        paginator = StandardResultsSetPagination()
        paginated_queryset = paginator.paginate_queryset(filtered_queryset, request)

        serializer = ReviewSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def populate_movies(request):
    """
    This view is not included in the URLs. 
    This was a sample function to populate the database with movies to test out pagination and filtering.
    """
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={settings.TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies_added = []

        for movie_data in data['results']:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'description': movie_data['overview'],
                    'release_date': movie_data['release_date'],
                    'poster': f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}"
                }
            )
            if created:
                movies_added.append(movie)

        serializer = MovieSerializer(movies_added, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to fetch data from TMDb"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
