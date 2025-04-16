from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product,Review
from .serializers import (CategorySerializer,CategoryDetailSerializer ,
                          ProductSerializer, ProductDetailSerializer,
                          ReviewSerializer, ReviewDetailSerializer,
                          ProductWithReviewsSerializer)


@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)

    data = CategoryDetailSerializer(category).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()

    # Step 2: Serialize
    data = CategorySerializer(categories, many=True).data

    # Step 3: Return response
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)  # Ищем товар по ID
    except Product.DoesNotExist:
        return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

    # Сериализуем данные
    data = ProductDetailSerializer(product).data

    # Возвращаем ответ
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    products = Product.objects.all()  # Получаем все товары

    # Сериализуем данные
    data = ProductSerializer(products, many=True).data

    # Возвращаем ответ
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()  # Получаем все отзывы

    # Сериализуем данные
    data = ReviewSerializer(reviews, many=True).data

    # Возвращаем ответ
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)  # Ищем отзыв по ID
    except Review.DoesNotExist:
        return Response({"error": "Отзыв не найден"}, status=status.HTTP_404_NOT_FOUND)

    # Сериализуем данные
    data = ReviewDetailSerializer(review).data

    # Возвращаем ответ
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()  # Получаем все товары

    data = ProductWithReviewsSerializer(products, many=True).data

    # Возвращаем ответ
    return Response(data=data, status=status.HTTP_200_OK)

