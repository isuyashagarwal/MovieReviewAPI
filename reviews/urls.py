from django.urls import path
from .views import read_reviews, create_reviews, review_detail

urlpatterns = [
    path('', read_reviews, name='Read Review'),
    path('create/', create_reviews, name="Create Review"),
    path('<int:pk>/', review_detail, name='review_detail'),
]