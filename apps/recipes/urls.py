from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecipeList.as_view(), name='index'),
    path('favorites/', views.FavoritesList.as_view(), name='favorites'),
    path('<str:username>/recipes/', views.AuthorList.as_view(),
         name='authorlist'),
    path('purchases/', views.PurchaseList.as_view(),
         name='purchases'),
    path('subscriptions/', views.FollowList.as_view(),
         name='subscriptions'),
    path('<str:username>/recipe/<slug:slug>/',
         views.RecipeDetail.as_view(),
         name='recipe'),
    path('<str:username>/recipe/<slug:slug>/edit/',
         views.add_or_edit_recipe,
         name='edit_recipe'),
    path('<str:username>/recipe/<slug:slug>/confirm/',
         views.delete_confirm,
         name='delete_confirm'),
    path('<str:username>/recipe/<slug:slug>/delete/',
         views.delete_recipe,
         name='delete_recipe'),
    path('add-recipe/',
         views.add_or_edit_recipe,
         name='add_recipe'),
    path('subscriptions/download/',
         views.shoplist_pdf,
         name='shoplist_pdf'),
]
