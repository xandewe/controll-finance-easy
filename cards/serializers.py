from rest_framework import serializers
from .models import Card, CreditCardDetail


class CreditCardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardDetail
        fields = ["id", "due_date", "closing_date", "updated_at"]
        read_only_fields = ["updated_at"]


class CardSerializer(serializers.ModelSerializer):
    card_detail = CreditCardDetailSerializer(required=False)

    class Meta:
        model = Card
        fields = ["id", "card_name", "category", "card_detail"]

    def create(self, validated_data: dict):
        card_detail_data = validated_data.pop("card_detail", None)
        card = Card.objects.create(**validated_data)

        if card_detail_data:
            CreditCardDetail.objects.create(card=card, **card_detail_data)

        return card
