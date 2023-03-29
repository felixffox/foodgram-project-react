from django.contrib.auth import get_user_model
from django.db import models

from .models import Ingredient, Recipe, Tag

User = get_user_model


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=30,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name} {self.color}'

class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        db_index=True
    )
    unit = models.CharField(
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name} {self.unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.CharField(
        verbose_name='Название блюда',
        max_length=100
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=5000
    )
    image = models.ImageField(
        verbose_name='Иллюстрация',
        upload_to='recipe_images/'
    )
    ingredients = models.ManyToManyField(
        verbose_name='Ингредиенты блюда',
        related_name='recipes',
        to=Ingredient,
        through='recipes.AmountIngredient',
    )
    tags = models.ManyToManyField(
        verbose_name='Тег',
        related_name='recipes',
        to=Tag
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=0
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self) -> str:
        return f'{self.title}. Автор: {self.author.username}'


class AmountIngredients(models.Model):
    recipe = models.ForeignKey(
        verbose_name='В каких рецептах',
        related_name='ingredient',
        to=Recipe,
        on_delete=models.CASCADE
    )
    ingredients = models.ForeignKey(
        verbose_name='Связанные ингредиенты',
        related_name='recipe',
        to=Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        default=0
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe', )

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredients}'


class Favourites(models.Model):
    recipe = models.ForeignKey(
        verbose_name='Понравившиеся рецепты',
        related_name='in_fovourites',
        to=Recipe,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        related_name='favourites',
        to=User,
        on_delete=models.CASCADE
    )
    add_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'


class BuyLists():
    recipe = models.ForeignKey(
        verbose_name='Рецепты в списке покупок',
        related_name='in_buylist',
        to=Recipe,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name='Владелец списка покупок',
        related_name='buylists',
        to=User,
        on_delete=models.CASCADE
    )
    add_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'