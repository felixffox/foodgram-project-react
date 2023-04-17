from django.http import FileResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (AmountIngredients, BuyLists, Favourites,
                            Ingredient, Recipe, Tag)
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import MyUser, Subscriptions

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (AmountIngredientSerializer, IngredientSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          TagSerializer, UserSerializer,
                          UserSubscriptionsSerializer)

# TODO Подготовить фильтры, переопределить методы для вьюсетов через декоратор action

class MyUserViewSet(UserViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username', 'email')
    permission_classes = (AllowAny, )
    pagination_class = PageNumberPagination

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Subscriptions.objects.filter(user=user)
        page = self.paginate_queryset(queryset)
        serializer = UserSubscriptionsSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated, )
    )
    def subscribe(self, request, pk=None):
        author = get_object_or_404(MyUser, pk=pk)
        if request.method == 'POST':
            serializer = UserSubscriptionsSerializer(
                Subscriptions.objects.create(user=request.user, author=author),
                context={'request': request},
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        Subscriptions.objects.filter(user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#class SubscribtionViewSet(viewsets.ModelViewSet):
#    serializer_class = UserSubscriptionsSerializer
#    permission_classes = (IsAuthenticated, )
#    pagination_class = PageNumberPagination
#    
#    def get_queryset(self):
#        return get_list_or_404(MyUser, following__user=self.request.user)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    #filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    #filterset_class = RecipeFilter
