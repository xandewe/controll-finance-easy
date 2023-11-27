from rest_framework import generics
from .serializers import TransactionSerializer
from .models import Transaction


class TransactionView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
