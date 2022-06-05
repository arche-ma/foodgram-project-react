from recipes.models import Ingredient, IngredientForRecipe
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.CharField(source='unit')

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.unit.name')

    class Meta:
        model = IngredientForRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class IngredientInputSerializer(serializers.Serializer):
    amount = serializers.IntegerField(write_only=True, min_value=1)
    id = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ('amount', 'id')

    def validate(self, attrs):
        if not Ingredient.objects.filter(pk=attrs['id']).exists():
            raise serializers.ValidationError(
                'Такого ингредиента не существует'
                )
        return super().validate(attrs)
