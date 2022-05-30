from django.urls import include, path
from rest_framework import routers

from .views import (RecipeViewSet, TagViewSet, IngredientViewSet,
                    SubscriptionsViewSet, SubscribeCreateDestroyViewSet,
                    FavoriteCreateDestroyViewSet, ShoppingCartViewSet, GetPDFView)


router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet, IngredientViewSet)
router.register('ingredients', IngredientViewSet)
router.register('users/subscriptions', SubscriptionsViewSet,
                basename='subscribe')
router.register(r'users/(?P<user_id>\d+)/subscribe',
                SubscribeCreateDestroyViewSet, basename='subscribe')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                FavoriteCreateDestroyViewSet, basename='favorite')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                ShoppingCartViewSet, basename='shopping_cart')

urlpatterns = [
    path(r'recipes/download_shopping_cart/',
         GetPDFView.as_view(), name='get_pdf'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]