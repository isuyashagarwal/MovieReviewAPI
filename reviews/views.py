from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from .filters import ReviewFilter
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def read_reviews(request):
    """
    Retrieves all reviews.

    Args:
    rating: int [optional], user: str[optional]

    Returns:
    Response: Returns a particular review.
    """

    if request.method == 'GET':
        reviews = Review.objects.all()
        filtered_queryset = ReviewFilter(request.GET, queryset=reviews).qs

        paginator = StandardResultsSetPagination()
        paginated_queryset = paginator.paginate_queryset(filtered_queryset, request)

        serializer = ReviewSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reviews(request):
    """
    Creates a review.

    Args:
    movie id: int, rating: int, comment: str. [POST Request]

    Returns:
    Response: Returns a particular review.
    """

    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail(request, pk):
    """
    Fetches a particular review on GET request, updates it on PUT request and deletes it on DELETE request.

    Args:
    review id: int.

    Returns:
    Response: Returns a particular review.
    """
    try:
        review = Review.objects.get(pk=pk, user=request.user)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ReviewSerializer(review, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)