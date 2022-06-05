from api.serializers.recipe_serializers import ShortRecipeSerializer
from recipes.models import Recipe
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .mixins import CreateDestroyViewSet


class ShoppingCartViewSet(CreateDestroyViewSet):

    id_endpoint = 'recipe_id'
    model = Recipe
    permission_classes = [IsAuthenticated,]

    def create(self, request, *args, **kwargs):
        user = request.user
        to_shopping_cart = self._get_entity_by_id()
        if to_shopping_cart in user.shopping_cart.all():
            return Response({'bad request': 'this recipe is already added'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.shopping_cart.add(to_shopping_cart)
        data = ShortRecipeSerializer(to_shopping_cart).data
        return Response(data=data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        in_shopping_cart = self._get_entity_by_id()
        user = request.user
        if in_shopping_cart not in user.shopping_cart.all():
            return Response(
                {'bad request': 'this recipe is not in your shopping cart'},
                status=status.HTTP_400_BAD_REQUEST)
        user.shopping_cart.remove(in_shopping_cart)
        return Response(status=status.HTTP_204_NO_CONTENT)
