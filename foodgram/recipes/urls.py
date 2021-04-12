from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/<slug:slug>/',
         views.recipe_view,
         name='recipe'),
]
