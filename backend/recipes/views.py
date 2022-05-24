from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import (Ingredient, Recipe, Favourite, IngredientAmount,
                     ShoppingCart, Tag)
from .serializers import (
    IngredientSerializer, RecipeSerializer,
    TagSerializer, ShoppingListSerializer,
    FavouriteSerializer)
from .filters import RecipeFilter, IngredientSearchFilter
from .permissions import IsOwnerOrReadOnly


class IngredientViewSet(viewsets.ModelViewSet):
    filter_backends = (IngredientSearchFilter,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [IsOwnerOrReadOnly, ]
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [IsOwnerOrReadOnly, ]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination
    #permission_classes = [IsOwnerOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated, ])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            user = request.user
            data = {
                'recipe': pk,
                'user': user.id
            }
            serializer = FavouriteSerializer(
                data=data,
                context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        Favourite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    filterset_class = RecipeFilter

    def post(self, request, pk):
        user = request.user
        data = {
            'recipe': pk,
            'user': user.id
        }
        context = {'request': request}
        serializer = ShoppingListSerializer(data=data,
                                            context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DonwloadShoppingCartViewSet(APIView):

    def get(self, request, pk=None):
        shopping_cart_relations = [
            ri_obj['recipe__id']
            for ri_obj in ShoppingCart.objects.filter(
                user=request.user).values('recipe__id')]
        ingredients = IngredientAmount.objects.values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(count=Sum('amount')).filter(
            recipe__id__in=shopping_cart_relations)

        file_content = ''
        file_content = '\n'.join(
            [f"({ingredient['ingredient__name']} \
            {ingredient['count']} \
            {ingredient['ingredient__measurement_unit']} \
            )" for ingredient in ingredients])

        response = HttpResponse(
            file_content,
            content_type='text/plain; charset=UTF-8'
        )
        response['Content-Disposition'] = (
            'attachment; filename=shopping_cart.txt')
        return response
