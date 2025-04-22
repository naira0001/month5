from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product,Review
from .serializers import (CategorySerializer,CategoryDetailSerializer ,
                          ProductSerializer, ProductDetailSerializer,
                          ReviewSerializer, ReviewDetailSerializer,
                          ProductWithReviewsSerializer,CategoryValidateSerializer,
                          ProductValidateSerializer,ReviewValidateSerializer)


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
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_name = serializer.validated_data['name']

        if Category.objects.exclude(id=category.id).filter(name=new_name).exists():
            return Response({'error': 'Категория с таким именем уже существует.'},
                            status=status.HTTP_400_BAD_REQUEST)

        category.name = new_name
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
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.create(
            name=serializer.validated_data['name']
        )
        return Response(
            data=CategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )

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
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category')

        product.save()

        return Response(status=status.HTTP_200_OK,
                        data=ProductDetailSerializer(product).data)


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
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.create(
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            price=serializer.validated_data['price'],
            category_id=serializer.validated_data['category']
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
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Получаем валидированные данные
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product')

        # Проверка: уже существует такой отзыв?
        if Review.objects.filter(text=text, product_id=product_id).exists():
            return Response(
                {"error": "Отзыв с таким текстом уже существует для этого товара."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Создаём отзыв
        review = Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id
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
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product')


        review.text = text
        review.stars = stars
        review.product_id = product_id
        review.save()

        return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()  # Получаем все товары
    data = ProductWithReviewsSerializer(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

