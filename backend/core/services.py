"""Служебные функции"""

from api.serializers import BuyListSerializer, FavouriteSerializer
from django.shortcuts import get_object_or_404
from recipes.models import BuyLists, Favourites, Recipe
from rest_framework import status
from rest_framework.response import Response


class ActionMethods:
    """Класс для экшн методов добавления и 
    удаления рецепта в корзину и избранное во вьюсетах"""
    def add_recipe(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if Favourites.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': ('Такой рецепт уже есть')},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        favorite = Favourites.objects.create(user=user, recipe=recipe)
        serializer = FavouriteSerializer(favorite.recipe)
        return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )

    def delete_recipe(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if not Favourites.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'errors': ('Такого рецепта нет')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Favourites.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def add_buylist_recipe(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if BuyLists.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': ('Такой рецепт уже есть')},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        buylist = BuyLists.objects.create(user=user, recipe=recipe)
        serializer = BuyListSerializer(buylist.recipe)
        return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )

    def delete_buylist_recipe(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if not BuyLists.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'errors': ('Такого рецепта нет')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        BuyLists.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
