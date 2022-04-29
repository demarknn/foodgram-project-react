from rest_framework import serializers

from food.models import Ingredient, Tag, Recipe, User


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


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UsersMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']

    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    # def update(self, instance, validated_data):
    #     user = super().update(instance, validated_data)
    #     try:
    #         user.set_password(validated_data['password'])
    #         user.save()
    #     except KeyError:
    #         pass
    #     return user



    def validate_username(self, value):
        if 'me' == value.lower():
            raise serializers.ValidationError(
                "Нельзя создавать пользователя ME"
            )
        if value == '':
            raise serializers.ValidationError("Нужно заполнить имя")
        return value

    def validate_email(self, value):
        if value == '':
            raise serializers.ValidationError("Нужно заполнить почту")
        return value
