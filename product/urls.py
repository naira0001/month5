from django.urls import path
from .views import (
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    ProductListCreateAPIView,
    ProductDetailAPIView,
    ReviewListCreateAPIView,
    ReviewDetailAPIView,
    ProductWithReviewsAPIView
)

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<int:id>/', CategoryDetailAPIView.as_view()),
    path('products/', ProductListCreateAPIView.as_view()),
    path('products/<int:id>/', ProductDetailAPIView.as_view()),
    path('reviews/', ReviewListCreateAPIView.as_view()),
    path('reviews/<int:id>/', ReviewDetailAPIView.as_view()),
    path('products/reviews/', ProductWithReviewsAPIView.as_view()),
]
