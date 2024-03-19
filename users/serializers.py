from rest_framework import serializers
from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    """ Список пользователей """

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    """ Создание пользователя """

    class Meta:
        model = User
        fields = ('email', 'password', 'telegram',)

    def create(self, validated_data):

        new_custom_user = User.objects.create_user(**validated_data)
        return new_custom_user
