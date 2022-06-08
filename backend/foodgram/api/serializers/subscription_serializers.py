from django.contrib.auth import get_user_model
from recipes.models import Recipe
from rest_framework.serializers import SerializerMethodField
from users.models import User

from .recipe_serializers import ShortRecipeSerializer
from .user_serializers import UserCreateSerializer


class SubscriptionsSerializer(UserCreateSerializer):
    recipes = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'recipes', 'is_subscribed')

    def get_recipes(self, user):
        limit = int(
            self.context['request'].query_params.get('recipes_limit', 10)
        )
        recipes = Recipe.objects.filter(author=user).order_by('-id')[:limit]
        serializer = ShortRecipeSerializer(instance=recipes,
                                           many=True)
        return serializer.data
