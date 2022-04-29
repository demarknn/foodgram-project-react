from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .views import (
    IngredientViewSet, RecipeViewSet,
    TagViewSet
)

v1_router = SimpleRouter()
v1_router.register('ingredient', IngredientViewSet)
v1_router.register('recipe', RecipeViewSet)
v1_router.register('tag', TagViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),

]
