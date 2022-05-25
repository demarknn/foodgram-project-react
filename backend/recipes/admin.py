from django.contrib import admin

from .models import (
    Ingredient, Recipe, Tag, IngredientAmount,
    Favourite, ShoppingCart)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favourite')
    list_filter = ('author', 'name', 'tags')

    def count_favourite(self, obj):
        return obj.favourite_recipe.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    ordering = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favourite)
admin.site.register(ShoppingCart)
admin.site.register(IngredientAmount)
