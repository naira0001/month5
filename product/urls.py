from django.urls import path
from .views import (
    category_list_create_api_view,
    category_detail_api_view,
    product_list_create_api_view,
    product_detail_api_view,
    review_list_create_api_view,
    review_detail_api_view,
    product_reviews_api_view,
)

urlpatterns = [
    # Categories
    path('categories/', category_list_create_api_view, name='category-list-create'),
    path('categories/<int:id>/', category_detail_api_view, name='category-detail'),

    # Products
    path('products/', product_list_create_api_view, name='product-list-create'),
    path('products/<int:id>/', product_detail_api_view, name='product-detail'),
    path('products/reviews/', product_reviews_api_view, name='product-reviews'),

    # Reviews
    path('reviews/', review_list_create_api_view, name='review-list-create'),
    path('reviews/<int:id>/', review_detail_api_view, name='review-detail'),
]