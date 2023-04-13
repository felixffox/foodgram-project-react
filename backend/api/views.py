from django.http import FileResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (AmountIngredients, BuyLists, Favourites,
                            Ingredient, Recipe, Tag)
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import MyUser, Subscriptions

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (AmountIngredientSerializer, IngredientSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          TagSerializer, UserSerializer,
                          UserSubscriptionsSerializer)

# TODO Подготовить фильтры и пагинатор

#class MyUserViewSet():
#    queryset = MyUser.objects.all()
#    serializer_class = UserSerializer
#    search_fields = ('username', 'email')
#    permission_classes = AllowAny

class SubscribtionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionsSerializer
    permission_classes = IsAuthenticated
    
    def get_queryset(self):
        return get_list_or_404(MyUser, following__user=self.request.user)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = IsAdminOrReadOnly

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = IsAdminOrReadOnly
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    #filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = IsAuthorOrReadOnly
    #pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    #filterset_class = RecipeFilter
