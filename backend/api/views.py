from rest_framework import viewsets
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

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


class UsersViewSet(UserViewSet):
    # queryset = User.objects.all()
    # serializer_class = UsersSerializer
    # # permission_classes = [AllowAny, ]
    # # filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    # search_fields = ('username', )
    # lookup_field = 'username'
    pagination_class = LimitOffsetPagination




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
