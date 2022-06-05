from api.views.favorite_views import FavoriteCreateDestroyViewSet
from api.views.get_csv_views import GetCSVView
from api.views.ingredient_views import IngredientViewSet
from api.views.recipe_views import RecipeViewSet
from api.views.shopping_cart_views import ShoppingCartViewSet
from api.views.subscription_views import (SubscribeCreateDestroyViewSet,
                                          SubscriptionsViewSet)
from api.views.tag_views import TagViewSet
from django.urls import include, path
from rest_framework import routers

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
         GetCSVView.as_view(), name='get_pdf'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
