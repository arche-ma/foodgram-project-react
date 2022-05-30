from django.contrib import admin

from .models import Recipe, Tag, Ingredient, Unit, IngredientForRecipe


class IngredientForRecipeInline(admin.TabularInline):
    model = IngredientForRecipe
    extra = 1


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientForRecipeInline, TagInline]
    exclude = ['tags']


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Unit)
admin.site.register(Recipe, RecipeAdmin)
