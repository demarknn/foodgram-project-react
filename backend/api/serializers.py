from rest_framework import serializers

from djoser.serializers import UserCreateSerializer, UserSerializer
from food.models import Ingredient, Tag, Recipe, User
from rest_framework.validators import UniqueValidator


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


# class UsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


class UsersMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'


class RegistrationSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'email', 'id', 'password', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class UsersSerializer(UserSerializer):
    #is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name')

    # class Meta:
    #     model = User
    #     fields = (
    #         'email', 'id', 'username', 'first_name', 'last_name',
    #         'is_subscribed')