from atexit import register
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from api.views import CategoryView, ChefView, CreateRecipeView, LoginView, RecipeView, RegisterView, ReviewView, SearchApiView, testdata

router = routers.DefaultRouter()

router.register(r'chef',ChefView)
router.register(r'category',CategoryView)
router.register(r'recipe',RecipeView)
# router.register(r'review',ReviewView)


urlpatterns = [
    path('',include(router.urls)),
    path('register/',RegisterView.as_view(),name = "Register Token"),
    path('crecipe/',CreateRecipeView.as_view(),name = "Create recipe"),
    path('crecipe/<int:pk>/',CreateRecipeView.as_view(),name = "Create2 recipe"),
    path('login/',LoginView.as_view(),name = "Login"),
    path('review/',ReviewView.as_view(),name = "Review"),
    path('testtoken/',testdata),
    path('search/',SearchApiView.as_view(),name = "Search")
]
