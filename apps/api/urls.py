"""`api` app URL Configuration."""
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('favorites', views.FavoritesView)
router.register('purchases', views.PurchaseView)
router.register('subscriptions', views.FollowView)

urlpatterns_api_v1 = [
    path('', include(router.urls)),
    path('ingredients/',
         views.api_get_ingredients,
         name='get_ingredients'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_api_v1)),
]
