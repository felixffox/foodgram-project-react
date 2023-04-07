"""Служебные функции"""

from recipes.models import AmountIngredients, Ingredient, Recipe


def recipe_ingredient_set(recipe: Recipe, ingredients: Ingredient) -> None:
    """Функция, которая записывает ингредиенты для конкретного рецепта.
    Связывает рецепт и ингредиент посредством модели количества ингредиентов"""
    objs = []

    for ingredient, amount in ingredients:
        objs.append(AmountIngredients(
            recipe=recipe,
            ingredients=ingredient,
            amount=amount
        ))

    AmountIngredients.objects.bulk_create(objs)