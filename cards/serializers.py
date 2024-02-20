from rest_framework import serializers
from .models import Card, CreditCardDetail


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ["id", "card_name", "category", "card_detail"]


class CreditCardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardDetail
        fields = ["id", "due_date", "closing_date", "updated_at"]
        read_only_fields = ["updated_at"]
