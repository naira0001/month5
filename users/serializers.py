from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SMSCode


# Базовый сериализатор для username и password
class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


# Сериализатор для регистрации
class UserRegisterSerializer(UserBaseSerializer):

    def validate_username(self, username):
        # Проверяем, что пользователь с таким username не существует
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('User already exists!')
        return username

    def create(self, validated_data):
        # Создаем пользователя
        username = validated_data['username']
        password = validated_data['password']

        user = User.objects.create_user(username=username, password=password)
        return user


# Сериализатор для авторизации
class UserAuthSerializer(UserBaseSerializer):
    pass


# Сериализатор для подтверждения
class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.RegexField(regex=r'^\d{6}$', max_length=6, min_length=6)

    def validate(self, data):
        username = data['username']
        code = data['code']

        try:
            # Проверяем, что пользователь существует
            user = User.objects.get(username=username)
            # Проверяем, что код подтверждения существует
            sms_code = SMSCode.objects.get(user=user, code=code)
        except User.DoesNotExist:
            raise serializers.ValidationError({'username': 'User not found.'})
        except SMSCode.DoesNotExist:
            raise serializers.ValidationError({'code': 'Invalid confirmation code.'})

        return data