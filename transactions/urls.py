from django.urls import path
from . import views

urlpatterns = [
    path("transactions/", views.TransactionView.as_view()),
    path("transactions/<int:pk>/", views.TransactionDetailView.as_view()),
    path("transactions/<int:pk>/tag/", views.TransactionTagDeleteView.as_view()),
]
