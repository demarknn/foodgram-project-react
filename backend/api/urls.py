from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .views import (
    IngredientViewSet, RecipeViewSet,
    TagViewSet, UsersViewSet
)

v1_router = SimpleRouter()
v1_router.register('ingredients', IngredientViewSet)
v1_router.register('recipes', RecipeViewSet)
v1_router.register('tags', TagViewSet)
v1_router.register(
    'users',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    
]
