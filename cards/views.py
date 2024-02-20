from rest_framework import generics
from .models import Card
from .serializers import CardSerializer


class CardView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer