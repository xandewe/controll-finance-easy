from rest_framework import generics
from rest_framework.views import APIView, Response, Request, status
from .serializers import TransactionSerializer
from .models import Transaction
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404


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
    type = filters.CharFilter(field_name="type", lookup_expr="iexact")
    tag = filters.CharFilter(field_name="tag__tag_name", lookup_expr="iexact")
    sub_tag = filters.CharFilter(field_name="tag__sub_tag_name", lookup_expr="iexact")
    status = filters.CharFilter(field_name="status", lookup_expr="iexact")
    year_month = filters.CharFilter(field_name="year_month_reference", lookup_expr="exact")

    class Meta:
        model = Transaction
        fields = ["type", "tag", "status", "year_month_reference"]


class TransactionView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionFilter


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionTagDeleteView(APIView):
    def delete(self, request: Request, pk):
        transaction_queryset = get_object_or_404(Transaction, pk=pk)

        transaction_queryset.tag = None
        transaction_queryset.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
