from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               related_name='recipes',
                               on_delete=models.CASCADE)
    in_favorites = models.ManyToManyField(User, related_name='favorites',
                                          blank=True)
    in_shopping_cart = models.ManyToManyField(User,
                                              related_name='shopping_cart',
                                              blank=True)
    name = models.CharField(verbose_name='Название',
                            unique=True,
                            max_length=255)
    image = models.ImageField(verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField('Ingredient',
                                         through='IngredientForRecipe',
                                         blank=False,
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField('Tag',
                                  verbose_name='Тэги', blank=False)
    cooking_time = models.SmallIntegerField(verbose_name='Время приготовления',
                                            validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Имя',
                            unique=True)
    slug = models.SlugField(verbose_name='Слаг',
                            unique=True)
    hex_code = models.CharField(verbose_name='Цвет',
                                max_length=7, default="#ffffff",
                                unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey('Ingredient',
                                   verbose_name='Ингредиент',
                                   on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Количество',
                                 validators=[MinValueValidator(1)],
                                 default=1)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        unique_together = ('ingredient', 'recipe')

    def __str__(self):
        return f'{self.ingredient.name} {self.amount}'


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=100)
    unit = models.ForeignKey('Unit', related_name='ingredients',
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Unit(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Единица измерения',
                            unique=True)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name
