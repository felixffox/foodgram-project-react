from django.contrib import admin

from .models import AmountIngredients, Ingredient, Recipe, Tag

EMPTY_VALUE = 'Значение не указано'

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author',)
    fields = (
        ('title', 'cooking_time'),
        ('author', 'tags'),
        ('description',),
        ('image',),
    )
    search_fields = ('author', 'title', 'tags')
    list_filter = ('author', 'title', 'tags')
    empty_value_display = EMPTY_VALUE
    save_on_top = True

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE
    save_on_top = True

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'color')
    empty_value_display = EMPTY_VALUE
    save_on_top = True

admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(AmountIngredients)
