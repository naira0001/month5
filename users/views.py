from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import SMSCode
from .serializers import UserRegisterSerializer, UserAuthSerializer, ConfirmSerializer
import secrets
from datetime import timedelta
from django.utils.timezone import now


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    # Создаем пользователя
    user = User.objects.create_user(username=username, password=password)

    # Генерируем 6-значный код подтверждения
    code = ''.join(secrets.choice('0123456789') for _ in range(6))

    # Сохраняем код в таблицу SMSCode
    SMSCode.objects.create(user=user, code=code)

    return Response(
        status=status.HTTP_201_CREATED,
        data={'message': 'User registered. Confirmation code generated.'}
    )



@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(username=username, password=password)

    if user:
        # Проверяем, активирован ли пользователь
        if SMSCode.objects.filter(user=user).exists():
            return Response(
                {'error': 'User is not confirmed!'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Создаем или получаем токен
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'key': token.key})

    return Response(
        {'error': 'Invalid credentials!'},
        status=status.HTTP_401_UNAUTHORIZED
    )


# Подтверждение пользователя
@api_view(['POST'])
def confirm_api_view(request):
    serializer = ConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    code = serializer.validated_data['code']

    try:
        user = User.objects.get(username=username)
        sms_code = SMSCode.objects.get(user=user, code=code)

        # Проверяем срок действия кода (например, 10 минут)
        if now() - sms_code.created_at > timedelta(minutes=10):
            sms_code.delete()
            return Response(
                {'error': 'Confirmation code expired.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Удаляем код после успешного подтверждения
        sms_code.delete()

        return Response(
            {'message': 'User confirmed successfully.'},
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    except SMSCode.DoesNotExist:
        return Response(
            {'error': 'Invalid confirmation code.'},
            status=status.HTTP_400_BAD_REQUEST
        )