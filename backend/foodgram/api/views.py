import csv

from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from django.contrib.auth import get_user_model

from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeInputSerializer, ShortRecipeSerializer, SubscriptionsSerializer,
                          TagSerializer)
from recipes.models import Recipe, Tag, Ingredient
from rest_framework.response import Response
from django.http import HttpResponse

from rest_framework import status
from rest_framework import permissions
from django.db.models import Count

from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class CreateDestroyViewSet(viewsets.GenericViewSet,
                           CreateModelMixin, DestroyModelMixin):

    def _get_entity_by_id(self):
        pk = self.kwargs.get(self.id_endpoint)
        instance = get_object_or_404(self.model, pk=pk)
        return instance


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly ]

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeInputSerializer
        return RecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.user
        is_favorited = self.request.query_params.get('is_favorited')
        print(is_favorited)
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
        if tags != []:
            queryset = queryset.annotate(
                count=Count('tags')).filter(count=len(tags))
            for tag in tags:
                queryset = queryset.filter(tags__slug=tag)
        return queryset


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    search_field = ('name')

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]


class SubscriptionsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return self.request.user.following.all()


class SubscribeCreateDestroyViewSet(CreateDestroyViewSet):

    id_endpoint = 'user_id'
    model = User
    permission_classes =[IsAuthenticated,]

    def get_serializer_class(self):
        return SubscriptionsSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        to_follow = self._get_entity_by_id()
        if to_follow == user:
            return Response({'error': 'you cannot follow yourself'},
                            status=status.HTTP_400_BAD_REQUEST)
        if to_follow in user.following.all():
            return Response(
                {'error': 'you\'re already following this account'},
                status=status.HTTP_400_BAD_REQUEST)
        user.following.add(to_follow)
        data = SubscriptionsSerializer(to_follow).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = request.user
        unfollow = self._get_entity_by_id()
        if unfollow not in user.following.all():
            return Response({'bad request': 'you don\'t follow this user'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.following.remove(unfollow)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteCreateDestroyViewSet(CreateDestroyViewSet, ):

    id_endpoint = 'recipe_id'
    model = Recipe
    permission_classes = [IsAuthenticated,]

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


class GetPDFView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        shopping_cart = request.user.shopping_cart.all()
        response = HttpResponse(content_type='text/csv')
        filename = f'{request.user.username}_items.csv'
        response['Content-Disposition'] = ('attachment;'
                                           f'filename="{filename}"')

        writer = csv.writer(response)
        for item in shopping_cart:
            writer.writerow([item.name])

            writer.writerow(['Ингредиент', 'Количество', 'Единица измерения'])
            for ingredient in item.ingredientforrecipe_set.all():
                writer.writerow(
                    [ingredient.ingredient.name, ingredient.quantity,
                     ingredient.ingredient.unit]
                )
            writer.writerow(['____________'])

        return response
