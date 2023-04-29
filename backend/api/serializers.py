from django.contrib.auth import get_user_model
from django.db.models import F
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import AmountIngredients, Ingredient, Recipe, Tag
from rest_framework import serializers
from users.models import MyUser, Subscriptions

from .fields import Base64ImageField, Hex2NameColor

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    class Meta:
        model = MyUser
        fields = (
            'email',
            'password',
            'username',
            'first_name',
            'last_name',
        )
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
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
        read_only_fields = ('is_subscribed', )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is not None:
            current_user = request.user
            if current_user.is_authenticated:
                return Subscriptions.objects.filter(
                    user=current_user,
                    author=obj
                ).exists()
        return False


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscriptions
        fields = ('author', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        if limit:
            recipes = recipes[:int(limit)]
        serializer = SubscribeRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__', )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__', )


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = AmountIngredients
        fields = ('id', 'name', 'amount', 'measurement_unit')


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=AmountIngredients.objects.all()
    )

    class Meta:
        model = AmountIngredients
        fields = ('id', 'amount')


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class BuyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class ReadRecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeReadSerializer(
        source='ingredient',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited',
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart',
        read_only=True
    )
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
            'ingredients',
            'is_favorite',
            'is_in_shopping_cart',
        )

    def get_ingredients(self, recipe):
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingredient__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            in_favourites__user=user,
            id=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            in_buylist__user=user,
            id=obj.id
        ).exists()


class CreateRecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = IngredientRecipeCreateSerializer(
        many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )
        read_only_fields = ('author',)

    def to_representation(self, instance):
        return ReadRecipeSerializer(instance, context=self.context).data

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredient_list = []
        for ingredient in ingredients:

            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными')
            ingredient_list.append(ingredient)

        data['ingredients'] = ingredients
        return data

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                'Необходимо выбрать теги!')
        return tags

    def add_ingredients_and_tags(self, tags, ingredients, recipe):
        tags = self.initial_data.get('tags')
        recipe.tags.set(tags)
        for ingredient in ingredients:
            AmountIngredients.objects.create(
                recipe=recipe,
                ingredients_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        return recipe

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        return self.add_ingredients_and_tags(
            tags, ingredients, recipe
        )

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.add_ingredients_and_tags(
            tags, ingredients, instance
        )
        instance = super().update(instance, validated_data)
        return instance
