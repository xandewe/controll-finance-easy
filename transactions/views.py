from rest_framework import generics
from .serializers import TransactionSerializer
from .models import Transaction
from django_filters import rest_framework as filters


class TransactionView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("category",)
