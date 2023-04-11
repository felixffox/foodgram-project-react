from django.http import FileResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (AmountIngredients, BuyLists, Favourites,
                            Ingredient, Recipe, Tag)
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import MyUser, Subscriptions

from .serializers import (AmountIngredientSerializer, IngredientSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          TagSerializer, UserSerializer,
                          UserSubscriptionsSerializer)

# Create your views here.
