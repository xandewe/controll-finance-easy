from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path(
        "users/",
        views.UserView.as_view(),
        name="user-create",
    ),
    path(
        "users/login/",
        TokenObtainPairView.as_view(),
        name="user-login",
    ),
]
