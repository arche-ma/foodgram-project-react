from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient


class IngredientFilterSet(FilterSet):
    name = filters.CharFilter(field_name='name',
                              lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']
