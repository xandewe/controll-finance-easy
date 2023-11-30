from rest_framework import generics
from .serializers import TransactionSerializer
from .models import Transaction
from django_filters import rest_framework as filters


class TransactionFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category", lookup_expr="iexact")
    tag = filters.CharFilter(field_name="tag__tag_name", lookup_expr="iexact")

    class Meta:
        model = Transaction
        fields = ["category"]


class TransactionView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionFilter
