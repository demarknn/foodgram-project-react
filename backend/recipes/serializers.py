from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from users.serializers import FullUserSerializer
from .models import (Ingredient, Recipe, Favourite, IngredientAmount,
                     ShoppingCart, Tag)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    amount = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'amount')
        model = IngredientAmount


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class RecipePostSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True, max_length=None)
    tags = TagSerializer(read_only=True, many=True)
    author = FullUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(required=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'
        # fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
        #           'is_in_shopping_cart', 'name', 'image', 'text',
        #           'cooking_time')

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Нужен хоть один ингридиент для рецепта'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError('Ингридиенты должны '
                                                  'быть уникальными')
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Убедитесь, что значение количества '
                                    'ингредиента больше 0')
                })
        data['ingredients'] = ingredients
        return data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favourite__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()


    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientAmount.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance


class RecipeListSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(read_only=True, many=True)
    # author = FullUserSerializer(read_only=True)
    # ingredients = IngredientAmountSerializer(required=True, many=True)
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'
        # fields = (
        #     'id', 'tags', 'author', 'ingredients',

        #     'name', 'image', 'text', 'cooking_time'
        # )
        # #             'is_favorited', 'is_in_shopping_cart',

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favourite__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('recipe', 'user')
        model = Favourite


class ShoppingListSerializer(FavouriteSerializer):
    class Meta(FavouriteSerializer.Meta):
        model = ShoppingCart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в список покупок'
            )
        ]
