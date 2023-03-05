"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

# We use the DefaultRouter with an APIView to automatically create
# views for all the options available.
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register("recipes", views.RecipeViewSet)

app_name = "recipe"

urlpatterns = [path("", include(router.urls))]
