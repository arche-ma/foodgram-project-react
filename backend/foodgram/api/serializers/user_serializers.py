from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import User


class UserCreateSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and obj in user.following.all())
