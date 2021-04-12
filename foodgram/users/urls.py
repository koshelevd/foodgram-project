"""Application 'users' URL Configuration."""
from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path("test/", views.test, name="test"),
]