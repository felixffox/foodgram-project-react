"""Служебные функции"""

from django.shortcuts import get_object_or_404
from recipes.models import AmountIngredients, Ingredient, Recipe
from rest_framework import status
from rest_framework.response import Response


class ActionMethods:
    """Класс для экшн методов добавления и 
    удаления рецепта в корзину и избранное во вьюсетах"""
    def add_recipe(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])
        user = request.user
        if Recipe.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': ('Такой рецепт уже есть')},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        Recipe.objects.create(user=user, recipe=recipe)
        return Response(
                self.recipe.data,
                status=status.HTTP_201_CREATED,
            )

    def delete_recipe(request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])
        user = request.user
        if not Recipe.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'errors': ('Такого рецепта нет')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Recipe.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
