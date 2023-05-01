from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (AmountIngredients, BuyLists, Favourites, Ingredient,
                     Recipe, Tag)

EMPTY_VALUE = 'Значение не указано'


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name', )
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE
    save_on_top = True


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author',)
    fields = (
        ('name', 'cooking_time'),
        ('author', 'tags'),
        ('text',),
        ('image',),
    )
    search_fields = ('author', 'name', 'tags')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = EMPTY_VALUE
    save_on_top = True


#class IngredientAdmin(admin.ModelAdmin):
#    list_display = ('name', 'measurement_unit')
#    search_fields = ('name',)
#    list_filter = ('name',)
#    empty_value_display = EMPTY_VALUE
#    save_on_top = True


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'color')
    empty_value_display = EMPTY_VALUE
    save_on_top = True


class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'add_date')
    search_fields = ('user', 'recipe')


class BuyListsAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'add_date')
    search_fields = ('user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(AmountIngredients)
admin.site.register(Favourites, FavouritesAdmin)
admin.site.register(BuyLists, BuyListsAdmin)
