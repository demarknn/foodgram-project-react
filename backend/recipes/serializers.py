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




class RecipeSerializer(serializers.ModelSerializer):
 """
    Data serializer for the Recipe model.
    """
    image = Base64ImageField()
    author = FullUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAmountSerializer(
        source="ingredients_amounts",
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "author", "tags", "text",
                  "ingredients", "cooking_time", "image",
                  "is_favorited", "is_in_shopping_cart")

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Favourite.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):

        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def validate(self, data: dict) -> dict:

        ingredients = self.initial_data.get("ingredients")
        set_ingredients = set()
        if not ingredients:
            raise serializers.ValidationError(
                "Make sure that at least one ingredient has been added"
            )
        else:
            for ingredient in ingredients:
                if int(ingredient.get("amount")) <= 0:
                    raise serializers.ValidationError(
                        ("Make sure the value of the amount "
                         "ingredient is greater than 0")
                    )
                ingredient_id = ingredient.get("id")
                if ingredient_id in set_ingredients:
                    raise serializers.ValidationError(
                        "The ingredient in the recipe must not be repeated."
                    )
                set_ingredients.add(ingredient_id)
        data["ingredients"] = ingredients

        tags = self.initial_data.get("tags")
        if not tags:
            raise serializers.ValidationError(
                "Make sure that at least one tag has been added"
            )
        elif tags:
            if Tag.objects.filter(id__in=tags).count() < len(tags):
                raise serializers.ValidationError(
                    "Some tag not exist in database."
                )
        data["tags"] = tags

        cooking_time = self.initial_data.get("cooking_time")
        if int(cooking_time) < 1:
            raise serializers.ValidationError(
                "Make sure that cooking time is grater then 0."
            )
        data["cooking_time"] = cooking_time

        return data

    def create(self, data: dict) -> Recipe:

        tags = data.pop("tags")
        image = data.pop("image")
        ingredients = data.pop("ingredients")
        recipe = Recipe.objects.create(image=image, **data)
        self.adding_tags_to_recipe(tags, recipe)
        self.save_ingredients_in_recipe(ingredients, recipe)

        return recipe

    def update(self, recipe: Recipe, data: dict) -> Recipe:

        recipe.tags.clear()
        tags = data.get("tags")
        self.adding_tags_to_recipe(tags, recipe)

        IngredientAmountSerializer.objects.filter(recipe=recipe).delete()
        ingredients = data.get("ingredients")
        self.save_ingredients_in_recipe(ingredients, recipe)

        if data.get("image") is not None:
            recipe.image = data.get("image")
        recipe.name = data.get("name")
        recipe.text = data.get("text")
        recipe.cooking_time = data.get("cooking_time")
        recipe.save()
        return recipe

    @staticmethod
    def adding_tags_to_recipe(tags, recipe):
        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))

    @staticmethod
    def save_ingredients_in_recipe(ingredients, recipe):
        for ingredient in ingredients:
            IngredientAmountSerializer.objects.create(
                recipe=recipe,
                ingredients_id=ingredient.get("id"),
                amount=ingredient.get("amount")
            )
# class RecipeSerializer(serializers.ModelSerializer):

#     tags = TagSerializer(read_only=True, many=True)
#     #author = FullUserSerializer(read_only=True)
#     #ingredients = IngredientAmountSerializer(many=True)
#     ingredients = serializers.SerializerMethodField()
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()

#     class Meta:
#         model = Recipe
#         fields = (
#             'id', 'tags', 'author', 'ingredients',
#             'is_favorited', 'is_in_shopping_cart',
#             'name', 'image', 'text', 'cooking_time'
#         )

#     def get_ingredients(self, obj):
#         recipe = obj
#         queryset = recipe.ingredients.all()
#         return IngredientAmountSerializer(queryset, many=True).data

#     def get_is_favorited(self, obj):
#         user = self.context.get('request').user
#         if user.is_anonymous:
#             return False
#         return Favourite.objects.filter(
#             recipe=obj,
#             user=user
#         ).exists()
#         #return Recipe.objects.filter(favourite__user=user, id=obj.id).exists()

#     def get_is_in_shopping_cart(self, obj):
#         user = self.context.get('request').user
#         if user.is_anonymous:
#             return False
#         return ShoppingCart.objects.filter(
#             recipe=obj,
#             user=user
#         ).exists()
#         #return ShoppingCart.objects.filter(cart__user=user, id=obj.id).exists()



# class RecipePostSerializer(serializers.ModelSerializer):
#     image = Base64ImageField(use_url=True, max_length=None)
#     tags = TagSerializer(read_only=True, many=True)
#     ingredients = IngredientAmountSerializer(required=True, many=True)


#     class Meta:
#         model = Recipe
#         fields = ('id', 'tags',  'ingredients', 
#                    'name', 'image', 'text',
#                   'cooking_time')


#     def validate(self, data):
#         ingredients = self.initial_data.get('ingredients')
#         if not ingredients:
#             raise serializers.ValidationError({
#                 'ingredients': 'Нужен хоть один ингридиент для рецепта'})
#         ingredient_list = []
#         for ingredient_item in ingredients:
#             ingredient = get_object_or_404(Ingredient,
#                                            id=ingredient_item['id'])
#             if ingredient in ingredient_list:
#                 raise serializers.ValidationError('Ингридиенты должны '
#                                                   'быть уникальными')
#             ingredient_list.append(ingredient)
#             if int(ingredient_item['amount']) < 0:
#                 raise serializers.ValidationError({
#                     'ingredients': ('Убедитесь, что значение количества '
#                                     'ингредиента больше 0')
#                 })
#         data['ingredients'] = ingredients
#         return data

#     def create_ingredients(self, ingredients, recipe):
#         for ingredient in ingredients:
#             IngredientAmount.objects.create(
#                 recipe=recipe,
#                 ingredient_id=ingredient.get('id'),
#                 amount=ingredient.get('amount'),
#             )

#     def create(self, validated_data):
#         image = validated_data.pop('image')
#         ingredients_data = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(image=image, **validated_data)
#         tags_data = self.initial_data.get('tags')
#         recipe.tags.set(tags_data)
#         self.create_ingredients(ingredients_data, recipe)
#         return recipe

#     def update(self, instance, validated_data):
#         instance.image = validated_data.get('image', instance.image)
#         instance.name = validated_data.get('name', instance.name)
#         instance.text = validated_data.get('text', instance.text)
#         instance.cooking_time = validated_data.get(
#             'cooking_time', instance.cooking_time
#         )
#         instance.tags.clear()
#         tags_data = self.initial_data.get('tags')
#         instance.tags.set(tags_data)
#         IngredientAmount.objects.filter(recipe=instance).all().delete()
#         self.create_ingredients(validated_data.get('ingredients'), instance)
#         instance.save()
#         return instance





# class RecipeSerializer(serializers.ModelSerializer):
#     image = Base64ImageField(use_url=True, max_length=None)
#     tags = TagSerializer(read_only=True, many=True)
#     author = FullUserSerializer(read_only=True)
#     ingredients = IngredientAmountSerializer(required=True, many=True)
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()

#     class Meta:
#         model = Recipe
#         fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
#                   'is_in_shopping_cart', 'name', 'image', 'text',
#                   'cooking_time')

#     def get_is_favorited(self, obj):
#         user = self.context.get('request').user
#         if user.is_anonymous:
#             return False
#         return Favourite.objects.filter(
#             recipe=obj,
#             user=user
#         ).exists()
#         #return Recipe.objects.filter(favourite__user=user, id=obj.id).exists()

#     def get_is_in_shopping_cart(self, obj):
#         user = self.context.get('request').user
#         if user.is_anonymous:
#             return False
#         return ShoppingCart.objects.filter(
#             recipe=obj,
#             user=user
#         ).exists()
#         #return ShoppingCart.objects.filter(cart__user=user, id=obj.id).exists()

#     def validate(self, data):
#         ingredients = self.initial_data.get('ingredients')
#         if not ingredients:
#             raise serializers.ValidationError({
#                 'ingredients': 'Нужен хоть один ингридиент для рецепта'})
#         ingredient_list = []
#         for ingredient_item in ingredients:
#             ingredient = get_object_or_404(Ingredient,
#                                            id=ingredient_item['id'])
#             if ingredient in ingredient_list:
#                 raise serializers.ValidationError('Ингридиенты должны '
#                                                   'быть уникальными')
#             ingredient_list.append(ingredient)
#             if int(ingredient_item['amount']) < 0:
#                 raise serializers.ValidationError({
#                     'ingredients': ('Убедитесь, что значение количества '
#                                     'ингредиента больше 0')
#                 })
#         data['ingredients'] = ingredients
#         return data

#     def create_ingredients(self, ingredients, recipe):
#         for ingredient in ingredients:
#             IngredientAmount.objects.create(
#                 recipe=recipe,
#                 ingredient_id=ingredient.get('id'),
#                 amount=ingredient.get('amount'),
#             )

#     def create(self, validated_data):
#         image = validated_data.pop('image')
#         ingredients_data = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(image=image, **validated_data)
#         tags_data = self.initial_data.get('tags')
#         recipe.tags.set(tags_data)
#         self.create_ingredients(ingredients_data, recipe)
#         return recipe

#     def update(self, instance, validated_data):
#         instance.image = validated_data.get('image', instance.image)
#         instance.name = validated_data.get('name', instance.name)
#         instance.text = validated_data.get('text', instance.text)
#         instance.cooking_time = validated_data.get(
#             'cooking_time', instance.cooking_time
#         )
#         instance.tags.clear()
#         tags_data = self.initial_data.get('tags')
#         instance.tags.set(tags_data)
#         IngredientAmount.objects.filter(recipe=instance).all().delete()
#         self.create_ingredients(validated_data.get('ingredients'), instance)
#         instance.save()
#         return instance


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
