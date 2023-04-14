from api.views import *
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
#router.register(r'users', MyUserViewSet)
#router.register(r'auth', MyUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]