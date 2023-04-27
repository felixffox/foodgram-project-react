"""Служебные функции"""

from api.serializers import ShortRecipeSerializer
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import status
from rest_framework.response import Response


class ActionMethods:
    """Класс для экшн методов добавления и 
    удаления рецепта в корзину и избранное во вьюсетах"""
    def add_obj(self, model, user, pk=None):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {'errors': ('Такой рецепт уже есть')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk=None):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': ('Такого рецепта нет')},
            status=status.HTTP_400_BAD_REQUEST,
        )
