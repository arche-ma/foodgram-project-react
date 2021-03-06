from django.contrib import admin

from .models import Ingredient, IngredientForRecipe, Recipe, Tag, Unit


class IngredientForRecipeInline(admin.TabularInline):
    model = IngredientForRecipe
    extra = 1


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientForRecipeInline, TagInline]
    exclude = ['tags']


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Unit)
