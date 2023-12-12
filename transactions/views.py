from rest_framework import generics
from .serializers import TransactionSerializer
from .models import Transaction
from django_filters import rest_framework as filters


class CustomDateFilter(filters.DateFilter):
    def filter(self, qs, value):
        if value:
            filter_lookups = {
                "%s__month" % (self.field_name,): value.month,
                "%s__year" % (self.field_name,): value.year,
            }
            qs = qs.filter(**filter_lookups)
        return qs


class TransactionFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category", lookup_expr="iexact")
    tag = filters.CharFilter(field_name="tag__tag_name", lookup_expr="iexact")
    sub_tag = filters.CharFilter(field_name="tag__sub_tag_name", lookup_expr="iexact")
    status = filters.CharFilter(field_name="status", lookup_expr="iexact")
    created_at = CustomDateFilter(field_name="created_at")

    class Meta:
        model = Transaction
        fields = ["category", "tag", "status", "created_at"]


class TransactionView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionFilter


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
