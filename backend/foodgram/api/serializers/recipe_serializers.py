from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientForRecipe, Recipe
from rest_framework import serializers

from .ingredient_serializers import (IngredientForRecipeSerializer,
                                     IngredientInputSerializer)
from .tag_serializers import TagSerializer
from .user_serializers import UserCreateSerializer


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientForRecipeSerializer(
        source='ingredientforrecipe_set',
        many=True)
    author = UserCreateSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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


class RecipeInputSerializer(serializers.ModelSerializer):

    ingredients = IngredientInputSerializer(many=True, required=True)
    image = Base64ImageField(required=True)
    name = serializers.CharField(max_length=150, required=True)
    cooking_time = serializers.IntegerField(required=True, min_value=1)
    text = serializers.CharField(max_length=1024, required=True)

    class Meta:
        model = Recipe
        fields = ['tags', 'ingredients', 'name',
                  'text', 'cooking_time', 'image']

    def validate(self, attrs):
        if (self.context['request'].method == 'POST'
                or self.instance.name != attrs['name']):
            if Recipe.objects.filter(name=attrs['name']).exists():
                raise serializers.ValidationError(
                    'Рецепт с таким названием уже существует')
        ingredient_ids = set()
        for ingredient in attrs['ingredients']:
            if ingredient['id'] in ingredient_ids:
                name = Ingredient.objects.get(pk=ingredient['id'])
                raise serializers.ValidationError(
                    f'{name}: Вы уже добавляли этот ингредиент')
            ingredient_ids.add(ingredient['id'])

        return super().validate(attrs)

    def create(self, validated_data):
        author = self.context['request'].user
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = Recipe.objects.create(author=author, image=image,
                                         **validated_data)

        for ingredient in ingredients:
            pk = ingredient.get('id')
            ingredient_object = get_object_or_404(Ingredient, pk=pk)
            IngredientForRecipe.objects.create(
                ingredient=ingredient_object,
                amount=ingredient.get('amount'),
                recipe=instance)
        instance.save()

        instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        image = validated_data.get('image', instance.image)
        instance.image = image
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.get('tags', instance.tags)
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.cooking_time = validated_data['cooking_time']
        instance.ingredients.clear()
        for ingredient in ingredients:
            instance.ingredients.add(
                Ingredient.objects.get(id=ingredient.get('id')),
                through_defaults={'amount': int(ingredient.get('amount'))}
            )
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


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
