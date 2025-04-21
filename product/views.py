from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product,Review
from .serializers import (CategorySerializer,CategoryDetailSerializer ,
                          ProductSerializer, ProductDetailSerializer,
                          ReviewSerializer, ReviewDetailSerializer,
                          ProductWithReviewsSerializer)


@api_view(['GET','PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailSerializer(category).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        category.name = request.data.get('name', category.name)
        category.save()
        return Response(data=CategoryDetailSerializer(category).data,
                        status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        name = request.data.get('name')

        category = Category.objects.create(
            name=name
        )
        return Response( status=status.HTTP_201_CREATED,
                         data=CategorySerializer(category).data)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)  # Ищем товар по ID
    except Product.DoesNotExist:
        return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category')
        product.save()
        return Response(data=ProductDetailSerializer(product).data,
                        status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Получаем данные из запроса
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category')  # foreign key

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )

        return Response(data=ProductDetailSerializer(product).data,
                        status=status.HTTP_201_CREATED)

@api_view(http_method_names=['GET','POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()  # Получаем все отзывы
        data = ReviewSerializer(reviews, many=True).data

        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Получаем данные из запроса
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product')  # Идентификатор товара, к которому привязан отзыв

        try:
            product = Product.objects.get(id=product_id)  # Находим товар по ID
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(
            text=text,
            stars=stars,
            product=product
        )

        return Response(data=ReviewDetailSerializer(review).data,
                        status=status.HTTP_201_CREATED)

@api_view(['GET','PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)  # Ищем отзыв по ID
    except Review.DoesNotExist:
        return Response({"error": "Отзыв не найден"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ReviewDetailSerializer(review).data

        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        review.text = request.data.get('text', review.text)
        review.stars = request.data.get('stars', review.stars)

        # Если нужно обновить товар:
        product_id = request.data.get('product')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                review.product = product
            except Product.DoesNotExist:
                return Response({"error": "Товар не найден"}, status=status.HTTP_400_BAD_REQUEST)

        review.save()
        return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()  # Получаем все товары
    data = ProductWithReviewsSerializer(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

