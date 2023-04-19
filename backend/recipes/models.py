from colorfield.fields import ColorField
from core.limits import Limits
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=Limits.LEN_NAME_LIMIT,
        unique=True
    )
    color = ColorField(
        format='hex',
        default='#FF0000',
        verbose_name='Цветовой HEX-код',
        max_length=Limits.LEN_HEX_CODE_LIMIT,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=Limits.LEN_NAME_LIMIT,
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
        max_length=Limits.LEN_NAME_LIMIT,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=Limits.LEN_NAME_LIMIT,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=Limits.LEN_NAME_LIMIT
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=Limits.LEN_TEXT_LIMIT
    )
    image = models.ImageField(
        verbose_name='Иллюстрация',
        upload_to='recipe_images/',
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name='Ингредиенты блюда',
        related_name='recipes',
        through='recipes.AmountIngredients',
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=0,
        validators=(
            MinValueValidator(
                Limits.MIN_COOKING_TIME,
                'Ваше блюдо уже готово!',
            ),
            MaxValueValidator(
                Limits.MAX_COOKING_TIME,
                'Очень долго ждать...',
            ),
        )
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
        return f'{self.name}. Автор: {self.author.username}'


class AmountIngredients(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        verbose_name='В каких рецептах',
        related_name='ingredient',
        on_delete=models.CASCADE
    )
    ingredients = models.ForeignKey(
        to=Ingredient,
        verbose_name='Связанные ингредиенты',
        related_name='recipe',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        default=0,
        validators=(
            MinValueValidator(
                Limits.MIN_AMOUNT_INGREDIENTS,
                message='Нужен хотя бы один ингредиент!'
            ),
            MaxValueValidator(
                Limits.MAX_AMOUNT_INGREDIENTS,
                message='Слишком много!'
            )
        )
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe', )

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredients}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Избранный автор',
        help_text='Избранный автор',
    )

    class Meta:
        verbose_name = 'Избранный автор'
        verbose_name_plural = 'Избранные авторы'

    def __str__(self):
        return f'{self.user} {self.author}'


class Favourites(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        verbose_name='Понравившиеся рецепты',
        related_name='in_fovourites',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User,
        verbose_name='Пользователь',
        related_name='favourites',
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


class BuyLists(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        verbose_name='Рецепты в списке покупок',
        related_name='in_buylist',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User,
        verbose_name='Владелец списка покупок',
        related_name='buylists',
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