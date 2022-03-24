from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsAdmin
from users.serializers import TokenSerializer, UserSerializer, UsersSerializer
from users.tokens import account_activation_token

MAIL_SUBJECT = 'Activation Token'
MAIL_ADDRESS = 'admin@superhost.com'
RESPONSE_MESSAGE = 'Activation Sended'
ERROR_RESPONSE_MESSAGE = 'Error in response'


@api_view(['POST'])
@permission_classes([AllowAny])
def validate_token(request):
    """Вью создания пользователя и отправки токена на почту"""
    serializer = UserSerializer(
        data=request.data
    )
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    user, is_created = User.objects.get_or_create(
        **serializer.data
    )
    token = account_activation_token.make_token(user)
    msg = render_to_string(
        template_name='users/mail_token_validate.html',
        context={
            'user': user,
            'token': token
        }
    )
    send_mail(
        MAIL_SUBJECT,
        msg,
        MAIL_ADDRESS,
        [user.email]
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение токена и валидация кода"""
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            ERROR_RESPONSE_MESSAGE,
            status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(
        User,
        username=serializer.data.get('username')
    )
    token_isvalid = account_activation_token.check_token(
        user=user,
        token=serializer.data.get('confirmation_code')
    )
    if token_isvalid:
        refresh = RefreshToken.for_user(user)
        return Response(
            data={
                'token': str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )
    return Response(
        ERROR_RESPONSE_MESSAGE,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def get_me(request):
    """Вью получения и изменения данных о себе"""
    if request.method == 'GET':
        serializer = UsersSerializer(
            instance=request.user,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    if request.method == 'PATCH':
        serializer = UsersSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not request.user.is_admin:
            serializer.save(
                role=request.user.role
            )
        else:
            serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделью пользователей"""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    permission_classes = (IsAdmin,)
