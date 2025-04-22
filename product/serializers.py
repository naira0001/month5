# product/serializers.py
from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    def get_products_count(self, obj):
         # Подсчитываем количество товаров в категории
        return obj.products.count()



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'title description price category'.split()

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text product stars'.split()

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'  # Для вывода всех полей отзыва

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)  # Все отзывы для товара
    rating = serializers.SerializerMethodField()  # Поле для среднего рейтинга

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def get_rating(self, obj):
        # Вычисляем средний рейтинг на основе отзывов
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.stars for review in reviews) / len(reviews)
        return 0


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=100)

    def validate_name(self, name):
        if Category.objects.filter(name=name).exists():
            raise ValidationError('Категория с таким именем уже существует.')
        return name

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=True)
    price = serializers.FloatField(min_value=0.01)
    category = serializers.IntegerField(min_value=1)

    def validate_title(self, title):
        if Product.objects.filter(title=title).exists():
            raise serializers.ValidationError('Такой товар уже существует.')
        return title

    def validate_category(self, category_id):
        if not Category.objects.filter(id=category_id).exists():
            raise serializers.ValidationError('Категория не найдена.')
        return category_id

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product = serializers.IntegerField()

    def validate_product(self, product_id):
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("Товар с таким ID не существует.")
        return product_id