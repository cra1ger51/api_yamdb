import re

from rest_framework.exceptions import ValidationError

from reviews.models import User


def validate_username(value):
    regex = re.compile(r'^[\w.@+-]+')
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя.')
    elif User.objects.filter(username=value).exists():
        raise ValidationError('Так уже представлялись. Это были не Вы?')
    elif not regex.match(value):
        raise ValidationError('Имя содержит недопустимые символы.')


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Пользователь с такой почтой '
                              'уже зарегестрирован')
