from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from .models import User
from .permissions import IsAdminOrSuperuserPermission
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsAdminOrSuperuserPermission)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def token_create(user):
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    response = {'token': str(token['access'])}
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Регистрация нового пользователя, отправка пода подтверждения.
    Формирование нового токена при повторной отправке запроса
    зарегистрированным пользователем.
    """
    serializer = SignUpSerializer(data=request.data)
    if User.objects.filter(username=request.data.get('username'),
                           email=request.data.get('email')).exists():
        user, created = User.objects.get_or_create(
            username=request.data.get('username')
        )
        if created is False:
            return token_create(user)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(username=request.data['username'],
                            email=request.data['email'])
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    send_mail(f'Уважаемый, {str(user.username)}! Код подтверждения:',
              f' Ваш код подтверждени: {confirmation_code}',
              settings.EMAIL_SENDER,
              [request.data['email']],
              fail_silently=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """
    Валидация кода подтверждения и формирование токена новому пользователю.
    """
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(User, username=request.data['username'])
        return token_create(user)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
