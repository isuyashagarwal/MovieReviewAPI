import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reviews.models import Review
from movie.models import Movie
from movie.serializers import MovieSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_movies(request):
    """
    Recommendation Engine Endpoint.

    Args:
    None

    Returns:
    A list of recommended movies
    """


    # Get all reviews
    reviews = Review.objects.all()

    # Prepare data for collaborative filtering
    users = list(reviews.values_list('user', flat=True).distinct())
    movies = list(reviews.values_list('movie', flat=True).distinct())
    user_index = {user: idx for idx, user in enumerate(users)}
    movie_index = {movie: idx for idx, movie in enumerate(movies)}

    # Create user-item matrix
    user_item_matrix = np.zeros((len(users), len(movies)))
    for review in reviews:
        user_idx = user_index[review.user.id]
        movie_idx = movie_index[review.movie.id]
        user_item_matrix[user_idx, movie_idx] = review.rating

    # Compute similarity between users
    user_similarity = cosine_similarity(user_item_matrix)

    # Get the index of the current user
    current_user_idx = user_index[request.user.id]

    # Compute weighted sum of ratings for all movies
    weighted_sum = user_similarity[current_user_idx, :].dot(user_item_matrix)
    normalization_factor = np.array([np.abs(user_similarity[current_user_idx, :]).sum()] * len(movies))
    scores = weighted_sum / normalization_factor

    # Get movie recommendations (excluding movies the user has already rated)
    recommendations = [
        movie for movie, score in sorted(zip(movies, scores), key=lambda x: x[1], reverse=True)
        if user_item_matrix[current_user_idx, movie_index[movie]] == 0
    ]

    # Serialize recommended movies
    recommended_movies = Movie.objects.filter(id__in=recommendations[:10])
    serializer = MovieSerializer(recommended_movies, many=True)
    print(recommendations)
    return Response(serializer.data)