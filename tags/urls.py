from django.urls import path
from . import views

urlpatterns = [
    path("tags/", views.TagView.as_view()),
    path("tags/<int:pk>/", views.TagDetailView.as_view()),
]
