from django.urls import path
from . import views

urlpatterns = [
    path(
        "cards/",
        views.CardView.as_view(),
        name="card-list-create",
    ),
]
