import io

from core.services import ActionMethods
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import AmountIngredients, Ingredient, Recipe, Tag
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import MyUser, Subscriptions

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserSerializer,
                          UserSubscriptionsSerializer)


class MyUserViewSet(UserViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username', 'email')
    permission_classes = (AllowAny, )
    pagination_class = PageNumberPagination

    @action(
        methods=['GET'],
        detail=False,
        url_path='subscriptions',
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, request):
        user = self.request.user
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
    def subscribe(self, request, id=None):
        author = get_object_or_404(MyUser, id=id)
        if request.method == 'POST':
            serializer = UserSubscriptionsSerializer(
                Subscriptions.objects.create(
                    user=request.user,
                    author=author
                ),
                context={'request': request},
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        Subscriptions.objects.filter(
            user=request.user,
            author=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    filterset_field = ('name', )

class RecipeViewSet(viewsets.ModelViewSet, ActionMethods):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('author', 'name', 'tags')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated, ),
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe(request, pk=pk)

        return self.delete_recipe(request, pk=pk)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated, ),
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_buylist_recipe(request, pk=pk)

        return self.delete_buylist_recipe(request, pk=pk)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.buylists.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        buylist = {}
        ingredients = AmountIngredients.objects.filter(
            recipe__in_buylist__user=request.user).values_list(
            'ingredients__name', 'ingredients__measurement_unit',
            'amount')
        for item in ingredients:
            name = item[0]
            if name not in buylist:
                buylist[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                buylist[name]['amount'] += item[2]


        pdfmetrics.registerFont(
            TTFont(
                'droid-serif',
                'fonts/droid-serif.ttf'
            )
        )
        buffer = io.BytesIO()  
        pdf_file = canvas.Canvas(buffer)
        pdf_file.setFont('droid-serif', 24)
        pdf_file.drawString(200, 800, 'Список покупок')
        pdf_file.setFont('droid-serif', 14)
        heigh = 750
        width = 75
        for i, (name, data) in enumerate(buylist.items(), 1):
            pdf_file.drawString(width, heigh, (
                f'{i}. {name} - {data["amount"]}, '
                f'{data["measurement_unit"]}'))
            heigh -= 25
        pdf_file.showPage()
        pdf_file.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename="shopping_list.pdf"
        )
