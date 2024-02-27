from django.urls import path
from . import views

urlpatterns = [
    path(
        "cards/<int:pk>/transactions/",
        views.TransactionView.as_view(),
        name="transaction-list-create",
    ),
    path(
        "transactions/<int:pk>/",
        views.TransactionDetailView.as_view(),
        name="transaction-detail",
    ),
    path(
        "transactions/<int:pk>/tag/",
        views.TransactionTagDeleteView.as_view(),
        name="transaction-delete-tag",
    ),
]
