#from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Follow, User
from recipes.models import Recipe
from recipes.serializers import CropRecipeSerializer

#dfssdfdf

class CustomUserCreateSerializer(UserCreateSerializer):
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


class FullUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()



class FollowUsersSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return CropRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()



# class FullUserSerializer(DjoserUserSerializer):
#     is_subscribed = serializers.SerializerMethodField(
#         'check_is_subscribed',
#         read_only=True
#     )

#     def check_is_subscribed(self, obj):
#         if self.context['request'].user.is_anonymous:
#             return False

#         if self.context['request'].user == obj:
#             return True

#         return Follow.objects.filter(
#             following=self.context['request'].user,
#             user=obj).exists

#     class Meta:
#         model = User
#         fields = list(DjoserUserSerializer.Meta.fields) + ['is_subscribed']
#         read_only_fields = (
#             list(
#                 DjoserUserSerializer.Meta.read_only_fields) + ['is_subscribed']
#         )


# class RecipeFollowUserField(serializers.Field):
#     def get_attribute(self, instance):
#         return Recipe.objects.filter(author=instance.following)


# class FollowUsersSerializer(serializers.ModelSerializer):
#     email = serializers.ReadOnlyField(source='following.email')
#     id = serializers.ReadOnlyField(source='following.id')
#     username = serializers.ReadOnlyField(source='following.username')
#     first_name = serializers.ReadOnlyField(source='following.first_name')
#     last_name = serializers.ReadOnlyField(source='following.last_name')
#     is_subscribed = serializers.ReadOnlyField(default=True)
#     recipes = RecipeFollowUserField()
#     recipes_count = serializers.IntegerField(
#         source='following.count',
#         read_only=True
#     )

#     class Meta:
#         read_only_fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes',
#             'recipes_count',
#         )
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes',
#             'recipes_count',
#         )
#         model = Follow
