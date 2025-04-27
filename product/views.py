from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, CategoryDetailSerializer,
    ProductSerializer, ProductDetailSerializer,
    ReviewSerializer, ReviewDetailSerializer,
    ProductWithReviewsSerializer,
    CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer
)

# Categories

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = Category.objects.create(
            name=serializer.validated_data['name']
        )
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'id'
    serializer_class = CategoryDetailSerializer

    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_name = serializer.validated_data['name']
        if Category.objects.exclude(id=category.id).filter(name=new_name).exists():
            return Response({'error': 'Категория с таким именем уже существует.'}, status=status.HTTP_400_BAD_REQUEST)

        category.name = new_name
        category.save()
        return Response(CategoryDetailSerializer(category).data, status=status.HTTP_200_OK)

# Products

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.create(
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            price=serializer.validated_data['price'],
            category_id=serializer.validated_data['category']
        )
        return Response(ProductDetailSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_class = ProductDetailSerializer

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data['title']
        product.description = serializer.validated_data['description']
        product.price = serializer.validated_data['price']
        product.category_id = serializer.validated_data['category']

        product.save()
        return Response(ProductDetailSerializer(product).data, status=status.HTTP_200_OK)

# Reviews

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data['text']
        stars = serializer.validated_data['stars']
        product_id = serializer.validated_data['product']

        if Review.objects.filter(text=text, product_id=product_id).exists():
            return Response(
                {"error": "Отзыв с таким текстом уже существует для этого товара."},
                status=status.HTTP_400_BAD_REQUEST
            )

        review = Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id
        )
        return Response(ReviewDetailSerializer(review).data, status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    lookup_field = 'id'
    serializer_class = ReviewDetailSerializer

    def put(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data['text']
        review.stars = serializer.validated_data['stars']
        review.product_id = serializer.validated_data['product']
        review.save()

        return Response(ReviewDetailSerializer(review).data, status=status.HTTP_200_OK)

# Product + Reviews

from rest_framework.views import APIView

class ProductWithReviewsAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = ProductWithReviewsSerializer(products, many=True).data
        return Response(data, status=status.HTTP_200_OK)
