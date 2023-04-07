import base64
from collections import OrderedDict

from core.services import recipe_ingredient_set
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db.models import F, QuerySet
from recipes.models import (AmountIngredients, BuyLists, Favourites,
                            Ingredient, Recipe, Tag)
from rest_framework import serializers

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

class ShortRecipeSerializer(serializers.ModelSerializer):
    """Усеченный набор полей сериализации Recipe
    для применения в некоторых эндпоинтах"""
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = 'is_subscribed'

    def get_is_subscribed(self, obj: User) -> bool:
        user = self.context.get('view').request.user
        
        if user.is_anonymous or (user == obj):
            return False

        return user.subscriptions.filter(author==obj).exists()

    def create(self, validated_data: dict) -> User:
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSubscriptionsSerializer(UserSerializer):
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = '__all__'

    def get_recipes_count(self, obj: User) -> int:
        return obj.recipes.count()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = (
            'is_favorite',
            'is_in_shopping_cart',
        )

    def get_ingredients(self, recipe: Recipe) -> QuerySet[dict]:
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('recipe__amount')
        )
        return ingredients

    def get_is_favourited(self, recipe: Recipe) -> bool:
        user = self.context.get('view').request.user

        if user.is_anonymous:
            return False

        return user.favourites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe: Recipe) -> bool:
        user = self.context.get('view').request.user

        if user.is_anonymous:
            return False

        return user.carts.filter(recipe=recipe).exists()

    def create(self, validated_data: dict) -> Recipe:
        return super().create(validated_data)