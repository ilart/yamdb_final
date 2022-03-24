from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField()


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email',)
            ),
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username',)
            )
        ]

    def validate_username(self, value):
        """
        Проверяем что пользователь не 'me'
        """
        if value == 'me':
            raise serializers.ValidationError(
                "Username must be different than 'me'"
            )
        return value


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email',)
            ),
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username',)
            )
        ]

    def validate_username(self, value):
        """
        Проверяем что пользователь не 'me'
        """
        if value == 'me':
            return self.context.get('request', None).user.username
        return value


class NotAdminUsersSerializer(UsersSerializer):

    class Meta:
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
        ]
        read_only_fields = [
            'role'
        ]
