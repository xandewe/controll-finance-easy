from django.urls import path
from . import views

urlpatterns = [
    path("transactions/tags/", views.TagView.as_view()),
    path("transactions/tags/<int:pk>/", views.TagDetailView.as_view()),
]
