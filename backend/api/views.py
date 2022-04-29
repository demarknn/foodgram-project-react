from rest_framework import viewsets
from rest_framework.response import Response
# from urllib import request
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.http import require_http_methods 

from food.models import Ingredient, Tag, Recipe, User
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    UsersSerializer,
    UsersMeSerializer,
    RegistrationSerializer
)
from api.permissions import (
    AdminAuthorOrReadOnly,
    AdminPermission,
    AdminOrReadOnly,
    AdminModeratorAuthorPermission,
)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = [AllowAny, ]
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination


    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        password = serializer.validated_data['password']
        try:
            User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        except Exception:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


@action(detail=False, methods=['GET', 'PATCH'], url_path='me',
        permission_classes=(AdminAuthorOrReadOnly,))
def me(self, request):
    serializer = UsersMeSerializer(request.user)
    userself = User.objects.get(username=self.request.user)
    if request.method == 'GET':
        serializer = self.get_serializer(userself)
        return Response(serializer.data)
    if request.method == 'PATCH':
        serializer = UsersMeSerializer(
            userself, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


