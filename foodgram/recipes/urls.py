from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/recipe/<slug:slug>/',
         views.recipe_view,
         name='recipe'),
    path('new-recipe/',
         views.new_recipe,
         name='new_recipe'),
    path('ingredients/',
         views.get_ing),
]
