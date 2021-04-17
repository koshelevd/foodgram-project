from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.RecipeList.as_view(), name='index'),
    # path('<str:username>/recipe/<slug:slug>/',
    #      views.recipe_view,
    #      name='recipe'),
    path('<str:username>/recipe/<slug:slug>/',
         views.RecipeDetail.as_view(),
         name='recipe'),
    path('<str:username>/recipe/<slug:slug>/edit/',
         views.add_or_edit_recipe,
         name='edit_recipe'),
    path('add-recipe/',
         views.add_or_edit_recipe,
         name='add_recipe'),
]
