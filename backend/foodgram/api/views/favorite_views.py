from api.serializers.recipe_serializers import ShortRecipeSerializer
from recipes.models import Recipe
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .mixins import CreateDestroyViewSet


class FavoriteCreateDestroyViewSet(CreateDestroyViewSet):

    id_endpoint = 'recipe_id'
    model = Recipe
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        return ShortRecipeSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        favorite = self._get_entity_by_id()
        if favorite in user.favorites.all():
            return Response({'bad request': 'this recipe is already added'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.favorites.add(favorite)
        data = ShortRecipeSerializer(favorite).data
        return Response(data=data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        favorite = self._get_entity_by_id()
        user = request.user
        if favorite not in user.favorites.all():
            return Response(
                {'bad request': 'this recipe is not in your favorites'},
                status=status.HTTP_400_BAD_REQUEST)
        user.favorites.remove(favorite)
        return Response(status=status.HTTP_204_NO_CONTENT)
