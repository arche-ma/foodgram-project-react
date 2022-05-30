from rest_framework.serializers import (ModelSerializer, CharField,
                                        ReadOnlyField, PrimaryKeyRelatedField,
                                        SerializerMethodField)
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe, Ingredient, IngredientForRecipe, Tag

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    is_subscribed = SerializerMethodField()

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


class TagSerializer(ModelSerializer):
    color = CharField(source='hex_code')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):
    measurement_unit = CharField(source='unit')

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientForRecipeSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.unit.name')

    class Meta:
        model = IngredientForRecipe
        fields = ['id', 'name', 'measurement_unit', 'quantity']


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientForRecipeSerializer(
        source='ingredientforrecipe_set',
        many=True)
    author = UserCreateSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'name',
                  'is_favorited', 'is_in_shopping_cart',
                  'image', 'text', 'cooking_time']

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj in user.favorites.all()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj in user.shopping_cart.all()


class RecipeInputSerializer(ModelSerializer):

    ingredients = IngredientForRecipeSerializer(many=True, required=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['tags', 'ingredients', 'name',
                  'text', 'cooking_time', 'image']

    def create(self, validated_data):
        author = self.context['request'].user
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = Recipe.objects.create(author=author, image=image,
                                         **validated_data)

        for ingredient in ingredients:
            IngredientForRecipe.objects.create(
                ingredient=ingredient['id'],
                quantity=ingredient['quantity'],
                recipe=instance)
        instance.save()

        instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop('image')
        instance.image = image
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.cooking_time = validated_data['cooking_time']
        instance.ingredients.clear()
        for ingredient in ingredients:
            IngredientForRecipe.objects.create(
                ingredient=ingredient['id'],
                quantity=ingredient['quantity'],
                recipe=instance)
        instance.tags.set(tags)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context['request']
        data = RecipeSerializer(instance,
                                context={'request': request}).data
        request = self.context.get('request')
        data['image'] = request.build_absolute_uri(instance.image.url)

        return data


class ShortRecipeSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class SubscriptionsSerializer(UserCreateSerializer):
    recipes = ShortRecipeSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'recipes', 'is_subscribed')
