"""API app URL Configuration."""
from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (TokenObtainPairView,
#                                             TokenRefreshView)
#
# from users.views import UserViewSet, api_user_create, send_token
#
# users_router = DefaultRouter()
# users_router.register('users', UserViewSet)
#
from rest_framework.routers import DefaultRouter

from . import views
from .views import FavoritesView, FollowView

router = DefaultRouter()

router.register('favorites', FavoritesView)
router.register('subscriptions', FollowView)

urlpatterns_api_v1 = [
    path('', include(router.urls)),
    path('ingredients/', views.api_get_ingredients,
         name='get_ingredients'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_api_v1)),
]
