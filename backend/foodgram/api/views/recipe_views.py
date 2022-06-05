from api.pagination import CustomPageNumberPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers.recipe_serializers import (RecipeInputSerializer,
                                                RecipeSerializer)
from recipes.models import Recipe
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeInputSerializer
        return RecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.user
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        author = self.request.query_params.get('author')
        tags = self.request.query_params.getlist('tags')

        if is_favorited is not None and is_favorited == '1':
            queryset = queryset.filter(in_favorites=user)

        if is_in_shopping_cart is not None and is_in_shopping_cart == '1':
            queryset = queryset.filter(in_shopping_cart=user)
        if author is not None:
            queryset = queryset.filter(author_id=author)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        return queryset.order_by('-id')
