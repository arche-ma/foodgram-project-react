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
        print(self.context)
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        if obj in user.following.all():
            return True
        return False
