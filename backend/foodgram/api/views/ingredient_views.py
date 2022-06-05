from api.serializers.ingredient_serializers import IngredientSerializer
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..filters import IngredientFilterSet


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilterSet
